import sys
import time
import mealpy as mp
import numpy as np
import random
from ....scheduler_alg.configuration import OptimizationConfiguration as conf

from ....scheduler_alg.business_logic.optimization_problem import SubsetOpProblemDefinition
from ....scheduler_alg.business_logic.optimization_problem import MyEliteMultiGA
from ....scheduler_alg.utils.convertors import FormattingUtils, MatrixOperations
from ....scheduler_alg.chart_engine import BuiltInCharts
from ..operations import ConsumptionOperations
from ...data_model.DTO.BuildingConfiguration import BuildingConfiguration


def do_subset(building_configuration, target_curve):
    problem_definition = build_problem(building_configuration, target_curve)

    start_time = time.time()
    best_solution, subset_model = solve_problem(problem_definition)
    end_time = time.time()
    print_elapsed_time(start_time, end_time)

    metrics = {}
    metrics["running_time"] = round(end_time - start_time, 2)
    metrics["upper_level_fitness"] = best_solution.target.objectives[0]
    metrics["lower_level_distance"] = problem_definition.best_metrics["avg_diff_kwh"]
    metrics["lower_level_comfort"] = problem_definition.best_metrics["avg_comfort"]
    # print(f"Best objectives from lower level: {problem_definition.best_problem_definition.normalized_fitness_values}")
    # print(
    #     f"Best adjusted upper level objectives:{best_solution.target.objectives}\nBest adjusted upper level fitness: {best_solution.target.fitness}")
    BuiltInCharts.draw_charts_from_model(subset_model, "subset")
    # BuiltInCharts.draw_charts_from_model(problem_definition.best_schedule_model, "schedule")

    best_schedule_configuration = problem_definition.best_schedule_configuration
    # schedule_evolution = get_schedule_evolution(problem_definition.best_schedule_model.best_agent_history, best_schedule_configuration.usage_matrix.shape)
    # SolutionEvolutionDiagram.drawEvolutionDiagram(best_schedule_configuration.consumption_vector, schedule_evolution, target_curve)

    best_schedule_solution_reshaped = MatrixOperations.reshape_flat_matrix(problem_definition.best_schedule_solution,
                                                                           best_schedule_configuration.usage_matrix.shape)

    schedule = best_schedule_solution_reshaped
    row_identifiers = np.array(list(best_schedule_configuration.appliances.keys()))

    schedule_not_included = np.zeros((1, 24))

    included_apartments_bitstring = best_solution.solution

    usage_matrix_not_included = np.zeros((1, 24))
    comfort_matrix_not_included = np.zeros((1, 24))
    consumption_vector_not_included = []
    appliances_not_included = []

    for id, appliance in building_configuration.appliances.items():
        apartment = id[0]
        if included_apartments_bitstring[apartment] == 0:
            usage_matrix_not_included = np.append(usage_matrix_not_included, [appliance.schedule_vector], axis=0)
            comfort_matrix_not_included = np.append(comfort_matrix_not_included, [appliance.comfort_vector], axis=0)
            consumption_vector_not_included = np.append(consumption_vector_not_included, [appliance.consumption], axis=0)
            row_identifiers = np.append(row_identifiers, [id], axis=0)

            appliances_not_included = np.append(appliances_not_included, [appliance], axis=0)

            # best_schedule_configuration.usage_matrix = np.append(best_schedule_configuration.usage_matrix,
            #                                                      [appliance.schedule_vector],
            #                                                      axis=0)
            # best_schedule_configuration.comfort_matrix = np.append(best_schedule_configuration.comfort_matrix,
            #                                                        [appliance.comfort_vector],
            #                                                        axis=0)
            # best_schedule_configuration.consumption_vector = np.append(best_schedule_configuration.consumption_vector,
            #                                                            [appliance.consumption], axis=0)
            #
            # schedule = np.append(schedule, [appliance.schedule_vector], axis=0)

            # schedule_not_included = np.append(schedule_not_included, [appliance.schedule_vector], axis=0)
            # consumption_vector_not_included = np.append(consumption_vector_not_included, [appliance.consumption], axis=0)

    buildingConfigurationNotIncluded = BuildingConfiguration()

    buildingConfigurationNotIncluded.appliances = np.append(best_schedule_configuration.appliances, appliances_not_included)
    buildingConfigurationNotIncluded.usage_matrix = np.append(best_schedule_configuration.usage_matrix, usage_matrix_not_included[1:], axis=0)
    buildingConfigurationNotIncluded.comfort_matrix = np.append(best_schedule_configuration.comfort_matrix, comfort_matrix_not_included[1:], axis=0)
    buildingConfigurationNotIncluded.consumption_vector = np.append(best_schedule_configuration.consumption_vector, consumption_vector_not_included, axis=0)
    schedule_all = np.append(schedule, usage_matrix_not_included[1:], axis=0)

    return best_solution.solution, schedule_all, buildingConfigurationNotIncluded, metrics, row_identifiers


def solve_problem(problem_definition):
    model = build_model()
    random_seed = random.randrange(sys.maxsize)
    no_processes = conf.upper_level_no_processes

    solution = model.solve(problem_definition, mode="single", n_workers=1, seed=random_seed)

    return solution, model


def build_model():
    epoch_number = conf.subset_epoch_number
    population_size = conf.subset_population_size
    crossover_probability = conf.subset_crossover_probability
    mutation_probability = conf.subset_mutation_probability

    optimization_model = MyEliteMultiGA.MyEliteMultiGA(epoch_number=epoch_number,
                                                       population_size=population_size,
                                                       crossover_probability=crossover_probability,
                                                       mutation_probability=mutation_probability)
    return optimization_model


def build_problem(building_configuration, target_curve):
    subset_weight = conf.subset_weight
    approximation_weight = conf.approximation_weight
    comfort_weight = conf.comfort_weight
    over_sampling_weight = conf.over_sampling_weight
    no_apartments = building_configuration.no_apartments

    return SubsetOpProblemDefinition.SubsetOpProblemDefinition(building_configuration=building_configuration,
                                                               target_curve=target_curve,
                                                               bounds=mp.BoolVar(no_apartments),
                                                               log_to=None,
                                                               obj_weights=[subset_weight, approximation_weight,
                                                                            comfort_weight, over_sampling_weight])


def print_elapsed_time(start, end):
    difference = end - start
    print(f"Elapsed time: {FormattingUtils.seconds_to_formatted_hour_minute_second(difference)} seconds")


def get_schedule_evolution(agent_evolution, shape):
    schedules = [MatrixOperations.reshape_flat_matrix(agent.solution, shape) for agent in agent_evolution]
    rounded_schedules = [np.where(schedule >= conf.discrete_transform_threshold, 1, 0) for
                         schedule in schedules]
    return rounded_schedules
