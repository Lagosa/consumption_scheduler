import numpy as np

from ....configuration import OptimizationConfiguration


def compute_objective(comfort_matrix, schedule):
    comfort_penalty = compute_total_comfort_penalty(comfort_matrix, schedule, compute_comfort_penalty)
    return comfort_penalty


def compute_total_comfort_penalty(comfort_matrix, schedule, penalty_function):
    scheduled_outside_comfort = np.multiply(comfort_matrix, schedule)
    comfort_vector_penalized = penalty_function(scheduled_outside_comfort)
    total_comfort_penalty = np.sum(comfort_vector_penalized)

    return total_comfort_penalty


def compute_comfort_penalty(comfort_violation):
    return (OptimizationConfiguration.comfort_penalty_base ** comfort_violation) - 1
