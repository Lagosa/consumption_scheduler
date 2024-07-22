import concurrent.futures
import copy
import random
import sys
import time
import multiprocessing

from ....scheduler_alg.utils.convertors import FormattingUtils, MatrixOperations
from mealpy import FloatVar
from ....scheduler_alg.business_logic.optimization_problem import ScheduleOpPrDef
from ....scheduler_alg.business_logic.optimization_problem import MyHHO
from ....scheduler_alg.business_logic.operations import ConsumptionOperations
from ....scheduler_alg.business_logic.optimization_problem.objective_functions import ComfortObjective
from ....scheduler_alg.business_logic.optimization_problem.objective_functions import \
    ConsumptionObjective
from ....scheduler_alg.business_logic.operations import ConstraintOperations

from ....scheduler_alg.utils.constants import RunningModes
from ....scheduler_alg.configuration import OptimizationConfiguration

from ....scheduler_alg.chart_engine import BuiltInCharts

import numpy as np
import matplotlib.pyplot as plt


def get_matrix_solution(building_configuration, target_curve):
    summation_offset = 0
    summation_correlation = 0
    best_solution_matrix_rounded = []
    model = None
    optimization_problem = None
    # for i in range(0, 1):
    # best_solution, model, optimization_problem = do_scheduling(building_configuration, target_curve)

    # usage_matrix_shape = building_configuration.usage_matrix.shape
    # best_solution_matrix = MatrixOperations.reshape_flat_matrix(best_solution.solution, usage_matrix_shape)
    # best_solution_matrix_rounded = np.where(best_solution_matrix >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)

    # BuiltInCharts.draw_charts_from_model(model, "schedule")
    # schedule_evolution = get_schedule_evolution(model.best_agent_history, usage_matrix_shape)
    # SolutionEvolutionDiagram.drawEvolutionDiagram(building_configuration.consumption_vector, schedule_evolution, target_curve)

    # summation_offset += optimization_problem.raw_fitness_values[0]
    # summation_correlation += optimization_problem.raw_fitness_values[1]
    # print(f"Avg. distance over 10 iterations: {summation_offset * 1.0 / 10}")
    # print(f"Avg. correlation over 10 iterations: {summation_correlation * 1.0 / 10}")

    # return best_solution_matrix_rounded, model, optimization_problem

    solution, metrics = do_scheduling_hourly(building_configuration, target_curve)

    return solution, metrics


def do_scheduling_hourly(building_configuration, target_curve):
    adjust_fitness = OptimizationConfiguration.should_adjust_fitness == 1
    fitness_approx = 0
    fitness_comf = 0
    running_time = 0

    best_solution_matr = []
    best_fitness = sys.maxsize
    n_best_distance_fitness = 0
    n_best_comfort_fitness = 0
    n_best_total_fitness = 0

    no_iterations = OptimizationConfiguration.first_level_no_iterations
    pool_size = OptimizationConfiguration.first_level_no_processes

    for i in range(0, no_iterations):
        solution = np.zeros((len(building_configuration.consumption_vector), 24))
        n_overday_distance_fitness = 0
        n_overday_comfort_fitness = 0
        n_overday_total_fitness = 0

        start = time.time()

        with multiprocessing.Manager() as manager:
            queue = manager.Queue()

            for hour in range(0, 24):
                seed = random.randrange(sys.maxsize)
                payload = {
                    "building_configuration": copy.deepcopy(building_configuration),
                    "target_curve": target_curve,
                    "hour": hour,
                    "seed": seed,
                    "adjust_fitness": adjust_fitness
                }
                queue.put(payload)

            with concurrent.futures.ProcessPoolExecutor(max_workers=pool_size) as executor:
                futures = [executor.submit(solve_multiprocessing, queue) for _ in range(0, 24)]
                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    subSolution, distance_obj, comfort_obj, fitness, hour = future.result()
                    np.copyto(solution[:, hour], subSolution.squeeze())
                    n_overday_distance_fitness += distance_obj
                    n_overday_comfort_fitness += comfort_obj
                    n_overday_total_fitness += fitness

        # for hour in range(0, 24):
        #     building_configuration_hourly = copy.deepcopy(building_configuration)
        #     solution_hourly, distance, comfort, fitness = solve_hourly(building_configuration_hourly, target_curve, hour,  None, adjust_fitness)
        #
        #     n_overday_total_fitness += fitness
        #     n_overday_distance_fitness += distance
        #     n_overday_comfort_fitness += comfort
        #
        #     np.copyto(solution[:, hour], solution_hourly.squeeze())

        solution = ConstraintOperations.apply_min_usage_hour_constraint(solution, building_configuration.constraint_matrix,
                                                   building_configuration.comfort_matrix)

        fitness_approx += ConsumptionObjective.apply_euclidean_distance(target_curve,
                                                                        ConsumptionOperations.compute_hourly_consumption(
                                                                            building_configuration.consumption_vector,
                                                                            solution))
        fitness_comf += ComfortObjective.compute_objective(building_configuration.comfort_matrix, solution)

        end = time.time()
        running_time += end - start

        if best_fitness > (fitness_approx + fitness_comf) / 2:
            best_fitness = (fitness_approx + fitness_comf) / 2
            best_solution_matr = solution
            n_best_distance_fitness = n_overday_distance_fitness
            n_best_comfort_fitness = n_overday_comfort_fitness
            n_best_total_fitness = n_overday_total_fitness
    # print(f"Avg. running time {running_time / no_iterations}")
    # print(f"Avg. Diff kWh {fitness_approx / no_iterations}")
    # print(f"Avg. Comfort {fitness_comf / no_iterations}")
    metrics = {
        "avg_running_time": round(running_time / no_iterations, 2),
        "avg_diff_kwh": round(fitness_approx / no_iterations, 2),
        "avg_comfort": round(fitness_comf / no_iterations, 2),
        "normalized_distance": round(n_best_distance_fitness / no_iterations, 2),
        "normalized_comfort": round(n_best_comfort_fitness / no_iterations, 2),
        "normalized_total_fitness": round(n_best_total_fitness / no_iterations, 2),
    }

    # best_solution_matr_rounded = np.where(best_solution_matr >= OptimizationConfiguration.discrete_transform_threshold,
    #                                       1, 0)
    return np.array(best_solution_matr), metrics


def do_scheduling(building_configuration, target_curve):
    adjust_fitness = OptimizationConfiguration.should_adjust_fitness == 1
    optimization_problem = build_problem(building_configuration, target_curve, adjust_fitness)

    start_time = time.time()
    best_solution, model = solve_problem(optimization_problem)
    end_time = time.time()
    running_time = end_time - start_time

    if OptimizationConfiguration.runtime_scenario == RunningModes.DO_FIRST_LEVEL_OPTIMIZATION:
        print_elapsed_time(start_time, end_time)
        print(f"Best objectives:{optimization_problem.raw_fitness_values}")
        print(f"Distance in kWh {optimization_problem.raw_fitness_values[0]}")
        print(
            f"\nBest adjusted objectives:{optimization_problem.normalized_fitness_values}\nBest adjusted fitness: {best_solution.target.fitness}\n\n")

    metrics = {
        "avg_running_time": round(running_time, 2),
        "avg_diff_kwh": round(optimization_problem.raw_fitness_values[0], 2),
        "avg_comfort": round(optimization_problem.raw_fitness_values[2], 2),
    }

    solution_matrix = MatrixOperations.reshape_flat_matrix(best_solution.solution, building_configuration.usage_matrix.shape)
    solution_matrix_rounded = np.where(solution_matrix > OptimizationConfiguration.discrete_transform_threshold, 1, 0)
    BuiltInCharts.draw_charts_from_model(model, "schedule")

    return np.array(solution_matrix_rounded), metrics


def do_handle_output(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"Received data for hour: {item[0]}")


def solve_multiprocessing(queue):
    payload = queue.get()

    solution, distance_obj, comfort_obj, fitness = solve_hourly(payload["building_configuration"],
                                                                payload["target_curve"], payload["hour"],
                                                                payload["seed"], payload["adjust_fitness"])
    return solution, distance_obj, comfort_obj, fitness, payload["hour"]


def solve_hourly(building_configuration_hourly, target_curve, hour, seed, adjust_fitness):
    building_configuration_hourly.usage_matrix = np.array(
        [building_configuration_hourly.usage_matrix[:, hour]]).reshape(-1, 1)
    building_configuration_hourly.comfort_matrix = np.array(
        [building_configuration_hourly.comfort_matrix[:, hour]]).reshape(-1, 1)

    optimization_problem = build_problem(building_configuration_hourly, target_curve[hour], adjust_fitness)
    best_solution, model = solve_problem(optimization_problem, seed)

    reshaped_matrix = MatrixOperations.reshape_flat_matrix(best_solution.solution,
                                                           (building_configuration_hourly.usage_matrix.shape[0], 1))
    solution = np.where(reshaped_matrix >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)

    return solution, best_solution.target.objectives[0], best_solution.target.objectives[1], best_solution.target.fitness



def build_problem(building_configuration, target_curve, adjust_fitness):
    initial_configuration = building_configuration.usage_matrix

    comfort_tradeoff = OptimizationConfiguration.comfort_tradeoff
    param_no = get_parameter_number(initial_configuration)

    target_curve_np = np.array(target_curve)

    hho_optimization_problem = get_problem_definition(building_configuration, target_curve_np, param_no,
                                                      1 - comfort_tradeoff, comfort_tradeoff, adjust_fitness)
    return hho_optimization_problem


def get_baseline_consumption(building_configuration, target_curve):
    # maximize the comfort objective => find a solution which maximizes the comfort objective
    problem_definition = build_problem(building_configuration, target_curve, False)
    problem_definition.obj_weights = [0, 1]
    best_solution, model = solve_problem(problem_definition)

    return problem_definition.raw_fitness_values[0], best_solution


def get_baseline_consumption_hourly(building_configuration, target_curve):
    building_configuration_hourly = copy.deepcopy(building_configuration)
    solution = [[0] for _ in range(0, building_configuration.usage_matrix.shape[0])]

    for hour in range(0, 24):
        building_configuration_hourly.usage_matrix = np.array([building_configuration.usage_matrix[:, hour]]).reshape(
            -1, 1)
        building_configuration_hourly.comfort_matrix = np.array(
            [building_configuration.comfort_matrix[:, hour]]).reshape(-1, 1)

        optimization_problem = build_problem(building_configuration_hourly, target_curve[hour], False)
        optimization_problem.obj_weights = [0, 1]
        best_solution, model = solve_problem(optimization_problem)

        reshaped_matrix = MatrixOperations.reshape_flat_matrix(best_solution.solution,
                                                               (building_configuration.usage_matrix.shape[0], 1))
        solution = np.hstack((solution, reshaped_matrix))

    solution = solution[:, 1:]
    rounded_solution = np.where(solution >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)
    solution = ConstraintOperations.apply_min_usage_hour_constraint(rounded_solution, building_configuration.constraint_matrix,
                                               building_configuration.comfort_matrix)

    fitness_approx = ConsumptionObjective.apply_euclidean_distance(target_curve,
                                                                   ConsumptionOperations.compute_hourly_consumption(
                                                                       building_configuration.consumption_vector,
                                                                       solution))
    fitness_comf = ComfortObjective.compute_objective(building_configuration.comfort_matrix, solution)

    return fitness_approx


def get_baseline_comfort(building_configuration, target_curve):
    # maximize consumption objective => find a solution which best approximates the curve, without considering the
    # comfort objective

    problem_definition = build_problem(building_configuration, target_curve, False)
    problem_definition.obj_weights = [1, 0]
    best_solution, model = solve_problem(problem_definition)

    return problem_definition.raw_fitness_values[2], best_solution


def get_baseline_comfort_hourly(building_configuration, target_curve):
    building_configuration_hourly = copy.deepcopy(building_configuration)
    solution = [[0] for _ in range(0, building_configuration.usage_matrix.shape[0])]

    for hour in range(0, 24):
        building_configuration_hourly.usage_matrix = np.array([building_configuration.usage_matrix[:, hour]]).reshape(
            -1, 1)
        building_configuration_hourly.comfort_matrix = np.array(
            [building_configuration.comfort_matrix[:, hour]]).reshape(-1, 1)

        optimization_problem = build_problem(building_configuration_hourly, target_curve[hour], False)
        optimization_problem.obj_weights = [1, 0]
        best_solution, model = solve_problem(optimization_problem)

        reshaped_matrix = MatrixOperations.reshape_flat_matrix(best_solution.solution,
                                                               (building_configuration.usage_matrix.shape[0], 1))
        solution = np.hstack((solution, reshaped_matrix))

    solution = solution[:, 1:]
    rounded_solution = np.where(solution >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)
    solution = ConstraintOperations.apply_min_usage_hour_constraint(rounded_solution, building_configuration.constraint_matrix,
                                               building_configuration.comfort_matrix)

    fitness_approx = ConsumptionObjective.apply_euclidean_distance(target_curve,
                                                                   ConsumptionOperations.compute_hourly_consumption(
                                                                       building_configuration.consumption_vector,
                                                                       solution))
    fitness_comf = ComfortObjective.compute_objective(building_configuration.comfort_matrix, solution)

    return fitness_comf


def get_problem_definition(building_configuration, target_curve, param_no,
                           weight_consumption_obj, weight_comfort_obj, adjust_fitness):
    return ScheduleOpPrDef.HHO(building_configuration=building_configuration,
                                           target_curve=[target_curve],
                                           should_normalize=adjust_fitness,
                                           bounds=FloatVar(lb=[0] * param_no, ub=[1] * param_no),
                                           log_to=None,
                                           obj_weights=[weight_consumption_obj, weight_comfort_obj])


def solve_problem(problem, seed=None):
    epoch_no = OptimizationConfiguration.schedule_epoch_no
    population_size = OptimizationConfiguration.schedule_population_size

    # optimization_model = HHO.OriginalHHO(epoch=epoch_no, pop_size=population_size)
    optimization_model = MyHHO.MyHHO(problem.building_configuration, epoch=epoch_no, pop_size=population_size)
    solution = run_without_initial_configuration(optimization_model, problem, seed)
    return solution, optimization_model


def run_without_initial_configuration(model, problem, seed=None):
    random_seed = seed
    if random_seed is None:
        random_seed = random.randrange(sys.maxsize)
    solution = model.solve(problem, mode="single", n_workers=1, seed=random_seed)
    return solution


def run_with_initial_configuration(model, problem, initial_configuration):
    flat_initial_configuration = get_flat_matrix(initial_configuration)
    population_size = OptimizationConfiguration.schedule_population_size
    initial_population_configuration = generate_initial_population_configuration(flat_initial_configuration,
                                                                                 population_size)

    solution = model.solve(problem, mode='thread', starting_solutions=initial_population_configuration)
    return solution


def generate_initial_population_configuration(initial_positions, population_size):
    population_configuration = []
    for i in range(population_size):
        population_configuration.append(initial_positions)
    return population_configuration


def draw_fitness_over_time(problem):
    plt.plot(range(len(problem.fitness_history)), problem.fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Fitness (Loss)")
    plt.title("Fitness Evolution over Time")
    plt.show()


def get_parameter_number(input_matrix):
    rows, cols = np.array(input_matrix).shape
    return rows * cols


def get_flat_matrix(matrix):
    return np.array(matrix).ravel()


def print_elapsed_time(start, end):
    difference = end - start
    print(f"Elapsed time: {FormattingUtils.seconds_to_formatted_hour_minute_second(difference)} seconds")
    print(f"In seconds: {difference}")


def get_schedule_evolution(agent_evolution, shape):
    schedules = [MatrixOperations.reshape_flat_matrix(agent.solution, shape) for agent in agent_evolution]
    rounded_schedules = [np.where(schedule >= OptimizationConfiguration.discrete_transform_threshold, 1, 0) for schedule
                         in schedules]
    return rounded_schedules
