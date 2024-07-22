import numpy as np
import matplotlib.pyplot as plt

from ..business_logic.operations import ConsumptionOperations
from . import LineDiagram
from . import DonutDiagram
from . import BarDiagram


def compareTotalConsumptionAndTarget(consumption, schedule, target_consumption, file_name="charts" +
                                                                                          "/approximation_metric.png",
                                     do_show_diagram=True):
    hourly_total_consumption = ConsumptionOperations.compute_hourly_consumption(consumption, schedule)
    data = np.stack((target_consumption, hourly_total_consumption), axis=0)

    x_label_values = range(24)
    row_label_values = ["Target curve", "Solution curve"]

    chartdetails = {
        "data_array": data,
        "x_label_values": x_label_values,
        "row_label_values": row_label_values,
        "plot_name": "Solution curve vs Target curve",
        "x_label": "Hours",
        "y_label": "kWh",
        "plot_file_name": file_name
    }
    LineDiagram.drawLineDiagram(chartdetails, show=do_show_diagram)


def count_ratio_of_devices_in_categories(devices, not_limit,
                                         mildly_limit, considerably_limit):
    no_not = 0
    no_mildly_affected = 0
    no_considerable_affected = 0
    no_severely_affected = 0

    for device in devices:
        if device <= not_limit:
            no_not = no_not + 1
            continue
        if device <= mildly_limit:
            no_mildly_affected = no_mildly_affected + 1
            continue
        if device <= considerably_limit:
            no_considerable_affected = no_considerable_affected + 1
            continue
        no_severely_affected = no_severely_affected + 1

    total_device_number = len(devices)

    return no_not * 1.0 / total_device_number, no_mildly_affected * 1.0 / total_device_number, no_considerable_affected * 1 / total_device_number, no_severely_affected * 1 / total_device_number


def count_devices_outside_comfort_hourly(solution, comfort_matrix):
    outside_comfort = np.multiply(solution, comfort_matrix)
    outside_comfort_marker = np.where(outside_comfort > 0, 1, 0)
    devices_outside_comfort_hourly = np.sum(outside_comfort_marker, axis=0)

    return devices_outside_comfort_hourly


def count_hours_outside_comfort_devicely(solution, comfort_matrix):
    outside_comfort = np.multiply(solution, comfort_matrix)
    outside_comfort_marker = np.where(outside_comfort > 0, 1, 0)
    hours_outside_comfort_devicely = np.sum(outside_comfort_marker, axis=1)

    return hours_outside_comfort_devicely


def count_hours_scheduled(solution, comfort_matrix):
    hours_outside_comfort_devicely = count_hours_outside_comfort_devicely(solution, comfort_matrix)
    count_hours_scheduled_devicely = np.sum(solution, axis=1)
    count_hours_inside_comfort_devicely = count_hours_scheduled_devicely - hours_outside_comfort_devicely
    return count_hours_inside_comfort_devicely


def get_ratio_devices_usage_percent_inside_comfort(solution, comfort_matrix):
    hours_outside_comfort_devicely = count_hours_outside_comfort_devicely(solution, comfort_matrix)
    count_hours_scheduled_devicely = np.sum(solution, axis=1)

    ratio_scheduled_outside_comfort = np.zeros(len(count_hours_scheduled_devicely))
    for index, x in enumerate(count_hours_scheduled_devicely):
        if count_hours_scheduled_devicely[index] > 0:
            ratio_scheduled_outside_comfort[index] = hours_outside_comfort_devicely[index] * 1.0 / \
                                                     count_hours_scheduled_devicely[index]

    four_quarters_in_comfort, three_quarters_in_comfort, half_in_comfort, one_quarter_in_comfort = count_ratio_of_devices_in_categories(
        ratio_scheduled_outside_comfort, 0.25, 0.5, 0.75)

    return four_quarters_in_comfort, three_quarters_in_comfort, half_in_comfort, one_quarter_in_comfort


def get_ratio_devices_comfort_interval_utilization(solution, comfort_matrix):
    no_comfort_hours_devicely = np.sum(np.where(comfort_matrix == 0, 1, 0), axis=1)

    count_hours_scheduled_devicely = np.sum(solution, axis=1)
    count_hours_inside_comfort_devicely = count_hours_scheduled(solution, comfort_matrix)

    ratio_inside_comfort_to_total_comfort_hours = np.zeros(len(no_comfort_hours_devicely))
    for index, x in enumerate(count_hours_scheduled_devicely):
        if no_comfort_hours_devicely[index] > 0:
            ratio_inside_comfort_to_total_comfort_hours[index] = count_hours_inside_comfort_devicely[index] * 1.0 / \
                                                                 no_comfort_hours_devicely[index]

    one_quarter_utilised, two_quarters_utilised, three_quarters_utilised, four_quarters_utilised = count_ratio_of_devices_in_categories(
        ratio_inside_comfort_to_total_comfort_hours, 0.25, 0.5, 0.75)

    return one_quarter_utilised, two_quarters_utilised, three_quarters_utilised, four_quarters_utilised


def drawComfortChart(solution, comfort_matrix):
    # number of hours a user is comfortable using a certain device

    devices_outside_comfort_hourly = count_devices_outside_comfort_hourly(solution, comfort_matrix)
    devices_outside_comfort_data = {
        "data_array": devices_outside_comfort_hourly,
        "x_label_values": range(0, 24),
        "row_label_values": ["Devices outside comfort"],
        "x_label": "Hours",
        "y_label": "No. devices outside comfort",
        "plot_name": "Number of devices outside comfort over the day",
        "plot_file_name": "devices_outside_comfort"
    }
    BarDiagram.drawBarDiagram(devices_outside_comfort_data)


    four_quarters_in_comfort, three_quarters_in_comfort, half_in_comfort, one_quarter_in_comfort = get_ratio_devices_usage_percent_inside_comfort(solution, comfort_matrix)
    one_quarter_utilised, two_quarters_utilised, three_quarters_utilised, four_quarters_utilised = get_ratio_devices_comfort_interval_utilization(solution, comfort_matrix)

    # out of scheduled hours how many are in the comfort interval
    ratio_of_comfort_in_scheduled_data = {
        "data_array": [four_quarters_in_comfort * 100, three_quarters_in_comfort * 100, half_in_comfort * 100,
                       one_quarter_in_comfort * 100],
        "colors": ["#EFB064", "#F3E9CC", "#A0A1B9", "#415688"],
        "labels": ["75%-100% in comfort interval", "50%-75% in comfort interval", "25%-50% in comfort interval",
                   "0%-25% in comfort interval"],
        "title": "% of devices having \n schedule in comfort interval"
    }

    # out of the comfort interval hours in how many is a device used
    extent_of_utilizing_the_comfort_interval = {
        "data_array": [four_quarters_utilised * 100, three_quarters_utilised * 100, two_quarters_utilised * 100,
                       one_quarter_utilised * 100],
        "colors": ["#EFB064", "#F3E9CC", "#A0A1B9", "#415688"],
        "labels": ["75%-100% in time interval", "50%-75% in time interval", "25%-50% in time interval",
                   "0%-25% in time interval"],
        "title": "% of devices having \n comfort interval utilized"
    }

    fig, plot = plt.subplots(1, 2, figsize=(6, 4), dpi=144)
    DonutDiagram.draw_diagram(plot, 0, ratio_of_comfort_in_scheduled_data)
    DonutDiagram.draw_diagram(plot, 1, extent_of_utilizing_the_comfort_interval)

    plt.savefig("charts/" + "comfort_evaluation" + ".png")
    plt.show()
    return None
