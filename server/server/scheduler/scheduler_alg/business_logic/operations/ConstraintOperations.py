import numpy as np

from ...utils.convertors import MatrixOperations
from ...configuration import OptimizationConfiguration


def apply_constraints(one_dimensional_solution, usage_matrix, constraint_matrix):
    solution = MatrixOperations.reshape_flat_matrix(one_dimensional_solution, usage_matrix.shape)

    deferrable_constraint = constraint_matrix[:, 0]
    solution = apply_deferrable_constraint(deferrable_constraint, solution, usage_matrix)

    # min_usage_hours_constraint = constraint_matrix[:, 1]
    # solution = apply_min_usage_hours_constraint(min_usage_hours_constraint, solution, usage_matrix)

    one_dimensional_solution = solution.flatten()
    return one_dimensional_solution


def apply_deferrable_constraint(constraint, solution, initial_configuration):
    constrained_solution = solution.copy()
    for index, isDeferrable in enumerate(constraint):
        if not isDeferrable:
            constrained_solution[index, :] = initial_configuration[index]

    return constrained_solution

def apply_min_usage_hour_constraint(solution, constraint_matrix, comfort_matrix):
    if OptimizationConfiguration.apply_min_usage_hour_constraint == 0:
        return solution

    for index, usage_row in enumerate(solution):
        usage = np.sum(usage_row)
        min_usage_hours = constraint_matrix[index][1]
        if usage >= min_usage_hours:
            continue

        rounded_usage_row = np.where(usage_row >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)
        comfort_row = comfort_matrix[index, :]
        comfort_row_normalized = np.where(comfort_row > 0, 0, 1)
        usage_row_neg = 1 - rounded_usage_row
        available_hours = np.bitwise_and(comfort_row_normalized, usage_row_neg.astype(int))
        hours_available_index = np.where(available_hours == 1)[0]

        hours_to_choose = min_usage_hours - usage
        chosen_hours = np.random.choice(hours_available_index, replace=False, size=int(hours_to_choose))
        for hour in chosen_hours:
            solution[index][hour] = 1
    return solution

# def apply_min_usage_hours_constraint(constraint, solution, initial_configuration):
#     constrained_solution = solution.copy()
#     for index, min_usage_hours in enumerate(constraint):
#         appliance_row = solution[index, :]
#         rounded_solution = np.where(appliance_row >= OptimizationConfiguration.discrete_transform_threshold, 1, 0)
#         usage_hours = np.sum(rounded_solution)
#         missing = min_usage_hours - usage_hours
#
#         i = 0
#         while i < missing:
#             rand_hour = random.randint(0, 23)
#             if rounded_solution[rand_hour] == 0:
#                 constrained_solution[index, rand_hour] = 1
#                 i = i + 1
#
#     return constrained_solution

