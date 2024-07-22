import numpy as np


def compute_total_consumption(usage_schedule):
    hourly_consumption = compute_hourly_consumption(usage_schedule)

    total_consumption = sum(hourly_consumption)
    return total_consumption


def compute_hourly_consumption(consumption, usage_schedule):
    scheduled_consumption = compute_scheduled_consumption(consumption, usage_schedule)
    hourly_consumption = np.sum(scheduled_consumption, axis=0)  # add column-wise the values

    return hourly_consumption


def compute_scheduled_consumption(consumption_vector, usage_schedule):
    consumption_vector_transposed = consumption_vector.reshape(-1, 1)
    scheduled_consumption = consumption_vector_transposed * usage_schedule

    return scheduled_consumption

