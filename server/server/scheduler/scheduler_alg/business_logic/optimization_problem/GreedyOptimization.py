import copy
import time

import numpy as np
from ..operations import ConsumptionOperations
from .objective_functions import ConsumptionObjective
from .objective_functions import ComfortObjective
from ...utils.convertors import FormattingUtils


class GreedyOptimization:

    def __init__(self, building_configuration, initial_solution, target_consumption):
        self.building_configuration = copy.deepcopy(building_configuration)
        self.solution = copy.deepcopy(initial_solution)
        self.target_consumption = target_consumption
        self.solution_consumption = []

    def solve(self, turn_on_non_deferrable):
        start_time = time.time()

        self.solution_consumption = ConsumptionOperations.compute_hourly_consumption(self.building_configuration.consumption_vector, self.solution)
        translation_table = self.make_translation_table()
        translation_table = self.remove_non_deferrable_devices(translation_table)

        for hour in range(0, 24):
            model_for_hour = self.extract_info_at_hour(translation_table, hour)
            gap, sign = compute_gap(self.solution_consumption, self.target_consumption, hour)

            if sign == 0:
                continue

            model_for_hour = self.remove_greater_consumption(model_for_hour, gap)

            if sign < 0:
                model_for_hour = self.remove_not_scheduled(model_for_hour)
                model_for_hour = self.sort_consumption_large_first(model_for_hour)
                model_for_hour = self.sort_not_in_comfort_first(model_for_hour)
                self.remove_devices(translation_table, model_for_hour, gap, hour)

            if sign > 0:
                model_for_hour = self.remove_scheduled(model_for_hour)
                model_for_hour = self.sort_consumption_large_first(model_for_hour)
                model_for_hour = self.sort_in_comfort_first(model_for_hour)
                self.add_devices(translation_table, model_for_hour, gap, hour)
        self.apply_min_usage_hour_constraint()
        end_time = time.time()
        running_time = end_time - start_time
        distanceApprox = ConsumptionObjective.apply_euclidean_distance(self.target_consumption, ConsumptionOperations.compute_hourly_consumption(self.building_configuration.consumption_vector, self.solution))
        comfortPenalty = ComfortObjective.compute_objective(self.building_configuration.comfort_matrix, self.solution)
        print("--- Greedy optimization ---\n")
        print(f"Elapsed time: {FormattingUtils.seconds_to_formatted_hour_minute_second(running_time)} seconds")
        print(f"In seconds: {running_time}")

        print(f"Distance in kWh: {distanceApprox}")
        print(f"Comfort penalty: {comfortPenalty}")

        return running_time, distanceApprox, comfortPenalty

    def apply_min_usage_hour_constraint(self):
        for index, usage_row in enumerate(self.solution):
            usage = np.sum(usage_row)
            min_usage_hours = self.building_configuration.constraint_matrix[index][1]
            if usage >= min_usage_hours:
                continue

            comfort_row = self.building_configuration.comfort_matrix[index, :]
            comfort_row_normalized = np.where(comfort_row > 0, 0, 1)
            usage_row_neg = 1 - usage_row
            available_hours = np.bitwise_and(comfort_row_normalized, usage_row_neg.astype(int))
            hours_available_index = np.where(available_hours == 1)[0]

            hours_to_choose = min_usage_hours - usage
            chosen_hours = np.random.choice(hours_available_index, replace=False, size=int(hours_to_choose))
            for hour in chosen_hours:
                self.solution[index][hour] = 1

    def sort_consumption_large_first(self, model):
        sorted_indices = np.argsort(model[:, 2], axis=0, kind="mergesort")
        return model[sorted_indices]

    def sort_not_in_comfort_first(self, model):
        sorted_indices = np.flip(np.argsort(model[:, 1], axis=0, kind="mergesort"))
        return model[sorted_indices]

    def sort_in_comfort_first(self, model):
        sorted_indices = np.argsort(model[:, 1], axis=0, kind="mergesort")
        return model[sorted_indices]

    def remove_greater_consumption(self, model, threshold):
        filter = model[:, 2] <= threshold
        return model[filter]

    def remove_not_scheduled(self, model):
        filter = model[:, 3] != 0
        return model[filter]

    def remove_scheduled(self, model):
        filter = model[:, 3] == 0
        return model[filter]

    def make_translation_table(self):
        return [[no,no] for no in range(0, len(self.building_configuration.consumption_vector))]

    def turn_on_non_deferrable_all_day(self, solution):
        for index, isDeferrable in enumerate(self.building_configuration.constraint_matrix[:, 0]):
            if isDeferrable == 0:
                for h in range(0, 24):
                    solution[index, h] = 1
        return solution

    def remove_non_deferrable_devices(self, translation_table):
        rows_to_remove = []
        for index, isDeferrable in enumerate(self.building_configuration.constraint_matrix[:, 0]):
            if isDeferrable == 0:
                rows_to_remove.append(index)
        translation_table_np = np.array(translation_table)
        translation_table_without_non_deferrable = np.delete(translation_table_np, rows_to_remove, axis=0)
        return translation_table_without_non_deferrable

    def extract_info_at_hour(self, translation_table, hour):
        extracted_info = []
        for index, [_, actual_index] in enumerate(translation_table):
            comfort = self.building_configuration.comfort_matrix[actual_index][hour]
            consumption = self.building_configuration.consumption_vector[actual_index]
            is_scheduled = self.solution[actual_index][hour]

            extracted_info.append([index, comfort, consumption, is_scheduled])

        return np.array(extracted_info)

    def unschedule(self, translation_table, model, device, hour):
        working_index = int(model[device][0])
        actual_device_index = translation_table[working_index][1]
        self.solution[actual_device_index][hour] = 0
        self.solution_consumption[hour] -= model[device][2]
        model[device][3] = 0

    def remove_devices(self, translation_table, model, gap, hour):
        current_device = 0
        while gap > 0 and current_device < len(model[:, 0]):
            consumption = model[current_device][2]
            if consumption < gap:
                self.unschedule(translation_table, model, current_device, hour)
                gap -= consumption
            current_device += 1

    def schedule_device(self, translation_table, model, device, hour):
        working_index = int(model[device][0])
        actual_device_index = translation_table[working_index][1]
        self.solution[actual_device_index][hour] = 1
        self.solution_consumption[hour] += model[device][2]
        model[device][3] = 1

    def add_devices(self, translation_table, model, gap, hour):
        current_device = 0
        while gap > 0 and current_device < len(model[:, 0]):
            consumption = model[current_device][2]
            if consumption < gap:
                self.schedule_device(translation_table, model, current_device, hour)
                gap -= consumption
            current_device += 1


def compute_gap(solution, target, hour):
    gap = target[hour] - solution[hour]
    sign = 0
    if gap < 0:
        sign = -1
    else:
        if gap > 0:
            sign = 1
    return np.abs(gap), sign
