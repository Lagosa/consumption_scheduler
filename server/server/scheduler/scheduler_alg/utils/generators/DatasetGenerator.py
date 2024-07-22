import copy
import random

import numpy as np

# device name, consumption kWh, isDeferrable, minHours
device_info = np.array([
    ["light", 0.06, 1, 3],
    ["fridge", 0.5, 0, 24],
    ["laptop", 0.065, 1, 3],
    ["microwave", 0.083, 1, 2]
])

usage_patterns = np.array([
    #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],  # at home in the morning
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]  # at home at evening
])

microwave_intervals = [
    [[8, 10], [11, 12], [21, 23]],
    [[7, 8], [18, 21]]
]

lighting_need = np.array([1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

apartment_configuration = np.array([
    [5, 1, 2, 1],  # apartment with 2 persons
    [5, 1, 4, 1]  # apartment with 4 persons
])

MAX_COMFORT_PENALTY = 2
comfort_penalty = [0, 1, 2]  # no penalty, small penalty, large penalty


def generate_dataset(no_apartments, type_ratio):
    building_device_info = []
    building_comfort = []
    building_usage = []

    ap_index = 0
    for type_index, ratio in enumerate(type_ratio):
        no_aps_in_type = int(no_apartments * ratio)

        for ap in range(0, no_aps_in_type):
            ap_info, ap_comfort, ap_usage = build_apartment(ap_index, type_index)
            building_device_info.extend(ap_info)
            building_comfort.extend(ap_comfort)
            building_usage.extend(ap_usage)

            ap_index += 1

    return np.array(building_device_info), np.array(building_comfort), np.array(building_usage)

def build_apartment(apartment_id, type):
    ap_device_info = []
    ap_device_comfort = []
    ap_device_usage = []

    device_configuration = apartment_configuration[type]
    device_index = 0
    for device_type_index, device_count in enumerate(device_configuration):

        for i in range(0, device_count):
            id = [apartment_id, device_index]
            info_row = copy.deepcopy(id)
            info_row.extend(device_info[device_type_index])

            ap_device_info.append(info_row)


            comfort_row = copy.deepcopy(id)
            comfort_row_raw = build_comfort_row(device_type_index, type)
            comfort_row.extend(comfort_row_raw)
            ap_device_comfort.append(comfort_row)

            usage_row = copy.deepcopy(id)
            usage_row.extend(build_usage_row(comfort_row_raw, device_type_index))
            ap_device_usage.append(usage_row)

            device_index += 1

    return ap_device_info, ap_device_comfort, ap_device_usage


def build_usage_row(comfort_row, device_type):
    max_usage_row = np.where(np.array(comfort_row) == 0, 1, 0)

    hours = int(device_info[device_type][3]) + random.randrange(0, 4)
    return build_row(max_usage_row, hours, 1, 0)


def build_comfort_row(device_type, apartment_type):
    if device_type == 0:
        return build_comfort_row_lighting(apartment_type)

    if device_type == 1:
        return build_comfort_row_fridge(apartment_type)

    if device_type == 2:
        return build_comfort_row_laptop(apartment_type)

    if device_type == 3:
        return build_comfort_row_microwave(apartment_type)


def build_comfort_row_fridge(apartment_type):
    return [0 for _ in range(0, 24)]


def build_comfort_row_lighting(apartment_type):
    possible_hours = np.bitwise_and(lighting_need, usage_patterns[apartment_type])
    min_hours = int(device_info[0][3])

    hours = min_hours + random.randrange(1, 4)

    return build_row(possible_hours, hours, comfort_penalty[0], comfort_penalty[MAX_COMFORT_PENALTY])


def build_comfort_row_laptop(apartment_type):
    hours = int(device_info[2][3]) + random.randrange(1, 4)
    return build_row(usage_patterns[apartment_type], hours, comfort_penalty[0], comfort_penalty[MAX_COMFORT_PENALTY])


def build_comfort_row_microwave(apartment_type):
    available_hour_index = [random.randrange(start, end) for start, end in microwave_intervals[apartment_type]]
    available_hours = [comfort_penalty[0] if np.isin(index, available_hour_index) else comfort_penalty[MAX_COMFORT_PENALTY] for index in range(0, 24)]
    return available_hours

def build_row(hourly_availability, no_hours_to_choose, value_if_chosen, value_if_not_chosen):
    possible_hours_index = np.where(hourly_availability == 1)[0]

    if no_hours_to_choose > len(possible_hours_index):
        no_hours_to_choose = len(possible_hours_index)

    hours_active_index = np.random.choice(possible_hours_index, replace=False, size=no_hours_to_choose)
    return [value_if_chosen if np.isin(index, hours_active_index) else value_if_not_chosen for index in range(0, 24)]
