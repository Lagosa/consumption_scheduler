import numpy as np

from ...operations import ConsumptionOperations
from scipy.stats import pearsonr


def compute_objective(consumption, schedule, target_curve):
    hourly_consumption = ConsumptionOperations.compute_hourly_consumption(consumption, schedule)
    return compute_deviation_from_target_hourly_consumption(target_curve, hourly_consumption)


def compute_deviation_from_target_hourly_consumption(target_curve, hourly_consumption):
    # pearson_coeff = apply_pearson_correlation_coefficient(target_curve, hourly_consumption)
    euclidean_dist = apply_euclidean_distance(target_curve, hourly_consumption)

    # return pearson_coeff, euclidean_dist
    return 1, euclidean_dist


def apply_pearson_correlation_coefficient(target_curve, hourly_consumption):
    person_correlation, p_value = pearsonr(np.array(target_curve[0]), hourly_consumption)
    return person_correlation


def apply_euclidean_distance(target_curve, hourly_consumption):
    hourly_deviation = np.abs(target_curve - hourly_consumption)
    total_deviation = np.sum(hourly_deviation)

    return total_deviation
