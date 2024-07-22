import sys

from mealpy import Problem
import numpy as np
from ...utils.convertors import MatrixOperations

from ...configuration import OptimizationConfiguration
from .objective_functions import ConsumptionObjective
from .objective_functions import ComfortObjective


class HHO(Problem):
    def __init__(self, building_configuration, target_curve,
                 should_normalize: True, bounds, log_to: None, obj_weights, **kwargs):
        self.building_configuration = building_configuration
        self.target_curve = target_curve
        self.should_normalize = should_normalize

        self.best_fitness = sys.maxsize
        self.normalized_fitness_values = []
        self.raw_fitness_values = []

        super().__init__(bounds=bounds, minmax="min", log_to=log_to, obj_weights=obj_weights, **kwargs)

    def obj_func(self, solution):
        initial_solution_shape = self.building_configuration.usage_matrix.shape
        reshaped_solution = MatrixOperations.reshape_flat_matrix(solution, initial_solution_shape)

        rounded_solution = np.where(reshaped_solution >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)

        raw_consumption_fitness_pearson, raw_consumption_fitness_euclidean = ConsumptionObjective.compute_objective(
            self.building_configuration.consumption_vector,
            rounded_solution,
            self.target_curve)
        raw_comfort_fitness = ComfortObjective.compute_objective(self.building_configuration.comfort_matrix, rounded_solution)

        aligned_consumption_fitness_pearson = 1 - raw_consumption_fitness_pearson

        if self.should_normalize:
            consumption_fitness_euclidean = normalize_euclidean_consumption_fitness(raw_consumption_fitness_euclidean)
            consumption_fitness_pearson = normalize_pearson_consumption_fitness(aligned_consumption_fitness_pearson)
            comfort_fitness = normalize_comfort_fitness(raw_comfort_fitness)
        else:
            consumption_fitness_euclidean = raw_consumption_fitness_euclidean
            consumption_fitness_pearson = aligned_consumption_fitness_pearson
            comfort_fitness = raw_comfort_fitness

        consumption_fitness = compute_consumption_fitness(consumption_fitness_euclidean, consumption_fitness_pearson)
        self.save_best_values(raw_consumption_fitness_euclidean,
                              raw_consumption_fitness_pearson,
                              raw_comfort_fitness,
                              consumption_fitness,
                              consumption_fitness_euclidean,
                              consumption_fitness_pearson,
                              comfort_fitness)

        return [consumption_fitness, comfort_fitness]

    def save_best_values(self, raw_consumption_fitness_euclidean, raw_consumption_fitness_pearson, raw_comfort_fitness,
                         consumption_fitness, consumption_fitness_euclidean, consumption_fitness_pearson,
                         comfort_fitness):
        fitness = compute_fitness(consumption_fitness_euclidean, consumption_fitness_pearson, comfort_fitness,
                                  self.obj_weights)
        if self.best_fitness > fitness:
            self.best_fitness = fitness
            self.raw_fitness_values = [raw_consumption_fitness_euclidean, raw_consumption_fitness_pearson,
                                       raw_comfort_fitness]
            self.normalized_fitness_values = [consumption_fitness_euclidean, consumption_fitness_pearson,
                                              consumption_fitness, comfort_fitness]


def compute_fitness(consumption_fitness_euclidean, consumption_fitness_pearson, comfort_fitness, weights):
    consumption_obj = compute_consumption_fitness(consumption_fitness_euclidean, consumption_fitness_pearson)
    fitness = np.dot([consumption_obj, comfort_fitness], weights)

    return fitness


def normalize_fitness(fitness, baseline, upper_limit):
    fitness_percent = fitness / baseline
    fitness_adjusted = fitness_percent * upper_limit
    return fitness_adjusted


def normalize_euclidean_consumption_fitness(fitness):
    return normalize_fitness(fitness,
                             OptimizationConfiguration.baseline_consumption_euclidean,
                             OptimizationConfiguration.fitness_reference_value)


def normalize_pearson_consumption_fitness(fitness):
    return normalize_fitness(fitness,
                             OptimizationConfiguration.baseline_consumption_pearson,
                             OptimizationConfiguration.fitness_reference_value)


def normalize_comfort_fitness(fitness):
    return normalize_fitness(fitness,
                             OptimizationConfiguration.baseline_comfort,
                             OptimizationConfiguration.fitness_reference_value)


def compute_consumption_fitness(euclidean_fitness, pearson_fitness):
    return (OptimizationConfiguration.weight_euclidean_obj_metric * euclidean_fitness
            + OptimizationConfiguration.weight_pearson_obj_metric * pearson_fitness)
