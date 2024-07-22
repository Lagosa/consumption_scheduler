import sys
import numpy as np

from mealpy import Problem

from ...data_model.DTO.BuildingConfiguration import BuildingConfiguration
from ..operations import SubsetOperations
from ..schedule_providers import ScheduleMaker
from ...configuration import OptimizationConfiguration


class SubsetOpProblemDefinition(Problem):
    def __init__(self, building_configuration, target_curve, bounds, log_to: None, obj_weights: [0.5, 0.5], **kwargs):
        self.schedule = []
        self.no_total_apartments = building_configuration.no_apartments
        self.building_configuration = building_configuration
        self.target_curve = target_curve
        self.best_schedule_solution = None
        self.best_schedule_configuration = None
        self.best_schedule_model = None
        self.best_problem_definition = None
        self.best_schedule_fitness = sys.maxsize
        self.best_metrics = {}

        super().__init__(bounds=bounds, minmax='min', log_to=log_to, obj_weights=obj_weights, **kwargs)

    def obj_func(self, solution):
        appliances_included, non_selected_consumption = SubsetOperations.get_appliances_according_to_subset(solution, self.building_configuration)

        new_target_curve = self.target_curve - np.array(non_selected_consumption)
        new_target_curve = np.where(new_target_curve < 0, 0, new_target_curve)

        no_hours_scheduled_too_much = 0
        for hour in range(0, 24):
            if self.target_curve[hour] < non_selected_consumption[hour]:
                no_hours_scheduled_too_much += 1

        over_selected_fitness = (no_hours_scheduled_too_much * 100.0) / 24

        new_building_configuration = BuildingConfiguration(appliances_included)
        schedule_solution, metrics = ScheduleMaker.do_scheduling_hourly(new_building_configuration, new_target_curve)

        no_apartments_included = sum(solution)
        subset_fitness = no_apartments_included * OptimizationConfiguration.fitness_reference_value / self.no_total_apartments
        schedule_fitness = compute_fitness(subset_fitness, metrics["normalized_distance"],
                                           metrics["normalized_comfort"], over_selected_fitness)

        self.save_solution(schedule_fitness, schedule_solution, new_building_configuration, metrics)


        return [subset_fitness, metrics["normalized_distance"], metrics["normalized_comfort"], over_selected_fitness]

    def save_solution(self, schedule_fitness, schedule_solution, schedule_configuration, metrics):
        if schedule_fitness < self.best_schedule_fitness:
            self.best_schedule_fitness = schedule_fitness
            self.best_schedule_solution = schedule_solution
            self.best_schedule_configuration = schedule_configuration
            self.best_metrics = metrics


def get_subset_fitness(solution, no_total_apartments):
    no_apartments_included = sum(solution)
    return no_apartments_included * OptimizationConfiguration.fitness_reference_value / no_total_apartments

def compute_fitness(subset_fitness, distance, comfort, over_selected_fitness):
    return OptimizationConfiguration.subset_weight * subset_fitness + \
        OptimizationConfiguration.approximation_weight * distance + \
        OptimizationConfiguration.comfort_weight * comfort + \
        OptimizationConfiguration.over_sampling_weight * over_selected_fitness
