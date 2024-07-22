import numpy as np
from ...scheduler_alg.business_logic.schedule_providers import SubsetMaker
from ...scheduler_alg.business_logic.operations import ConsumptionOperations
from ...scheduler_alg.configuration import InputConfiguration
from ...scheduler_alg.chart_engine import EvaluationDiagrams
from ...scheduler_alg.utils.convertors import FormattingUtils
from ...scheduler_alg.business_logic.optimization_problem.objective_functions import ConsumptionObjective
from ...scheduler_alg.business_logic.optimization_problem.objective_functions import ComfortObjective


def do(building_configuration, target_curve):
    subset, schedule, configuration, metrics, row_identifiers = SubsetMaker.do_subset(building_configuration, target_curve)

    print(f"Included apartments in the DR program: {sum(subset)}")
    apartments_included = [ap_id for ap_id, is_included in enumerate(subset) if is_included == 1]
    print(f"Included apartments: {apartments_included}")

    hourly_consumption_vector = ConsumptionOperations.compute_hourly_consumption(
        configuration.consumption_vector, schedule)

    # Solution vs Target
    rounded_hourly_consumption_vector = np.round(hourly_consumption_vector, 2)
    consumption_distance = ConsumptionObjective.apply_euclidean_distance(target_curve, rounded_hourly_consumption_vector)
    comfort_objective = ComfortObjective.compute_objective(configuration.comfort_matrix, schedule)
    hourly_label = np.array(range(0, 24))

    # Devices outside comfort hourly
    devices_outside_comfort_hourly = EvaluationDiagrams.count_devices_outside_comfort_hourly(
        schedule, configuration.comfort_matrix)
    devices_inside_comfort_hourly = building_configuration.comfort_matrix.shape[0] - devices_outside_comfort_hourly


    # Ratio of devices with utilization inside comfort
    labels_ratio_usage_percent_inside_comfort = ["100%-75% in comfort interval", "75%-50% in comfort interval",
                                                 "50%-25% in comfort interval", "25%-0% in comfort interval"]
    four_quarters_in_comfort, three_quarters_in_comfort, half_in_comfort, one_quarter_in_comfort = EvaluationDiagrams.get_ratio_devices_usage_percent_inside_comfort(
        schedule, configuration.comfort_matrix)

    # Ratio of devices with comfort interval utilization
    labels_ratio_comfort_interval_utilization = ["100%-75% in time interval", "75%-50% in time interval",
                                                 "50%-25% in time interval", "25%-0% in time interval"]
    one_quarter_utilised, two_quarters_utilised, three_quarters_utilised, four_quarters_utilised = EvaluationDiagrams.get_ratio_devices_comfort_interval_utilization(
        schedule, configuration.comfort_matrix)

    # Export solution
    # row_identifiers_not_included = [[0, 0]]
    # for ap_id, dev_id in building_configuration.appliances.keys():
    #     if subset[ap_id] == 0:
    #         row_identifiers_not_included = np.append(row_identifiers_not_included, [[ap_id, dev_id]], axis=0)
    #
    # row_identifiers_not_included = row_identifiers_not_included[1:]
    # row_identifiers_all = np.append(row_identifiers, row_identifiers_not_included, axis=0)

    augmented_solution_headers = np.array(
        ['Ap. id', 'Dev. id', 'H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
         'H10', 'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21',
         'H22', 'H23'])
    augmented_solution = np.hstack((row_identifiers, schedule))
    np.savetxt(InputConfiguration.output_location + "/" + InputConfiguration.output_solution + ".csv",
               augmented_solution, delimiter=",", fmt="%i", header=','.join(augmented_solution_headers))

    return {
        'status': "OPERATION_PERFORMED",
        'result': [
            {
                'type': "TABLE",
                'data':
                    {
                        'rows': [["Running time:", FormattingUtils.seconds_to_formatted_hour_minute_second(metrics["running_time"])],
                                 ["No. apartments selected:", sum(subset)],
                                 ["Apartments included", np.array(apartments_included)],
                                 ["Ap. selected from total", str(round(metrics["upper_level_fitness"], 1)) + "%"],
                                 ["Distance (kWh)", round(consumption_distance, 2)],
                                 ["Discomfort metric", comfort_objective]],
                        'header': [],
                        'title': "Upper level metrics"
                    }
            },
            {
                'type': "CHART",
                'data':
                    {
                        'label': hourly_label,
                        'type': 'LINE',
                        'yAxisTitle': 'Consumption (kWh)',
                        'xAxisTitle': 'Hour',
                        'title': 'Solution vs. Target consumption',
                        'valuesArray':
                            [
                                {
                                    'seriesName': 'Solution consumption',
                                    'seriesValues': rounded_hourly_consumption_vector
                                },
                                {
                                    'seriesName': 'Target consumption',
                                    'seriesValues': np.array(target_curve)
                                }
                            ]
                    }
            },
            {
                'type': "CHART",
                'data':
                    {
                        'label': hourly_label,
                        'type': 'BAR',
                        'yAxisTitle': 'No. devices',
                        'xAxisTitle': 'Hour',
                        'title': 'Number of devices outside comfort over the day',
                        'valuesArray':
                            [
                                {
                                    'seriesName': 'Devices outside comfort',
                                    'seriesValues': devices_outside_comfort_hourly
                                },
                                {
                                    'seriesName': 'Devices inside comfort',
                                    'seriesValues': devices_inside_comfort_hourly
                                }
                            ]
                    }
            },
            {
                'type': "CHART",
                'data':
                    {
                        'label': labels_ratio_usage_percent_inside_comfort,
                        'type': 'PIE',
                        'title': '% of devices having schedule in comfort interval',
                        'valuesArray': [
                            {
                                "seriesName": "",
                                "seriesValues": [round(four_quarters_in_comfort * 100, 2),
                                                 round(three_quarters_in_comfort * 100, 2),
                                                 round(half_in_comfort * 100, 2),
                                                 round(one_quarter_in_comfort * 100, 2)]
                            }
                        ]
                    }
            },
            {
                'type': "CHART",
                'data':
                    {
                        'label': labels_ratio_comfort_interval_utilization,
                        'type': 'PIE',
                        'title': '% of devices having comfort interval utilized',
                        'valuesArray': [
                            {
                                "seriesName": "",
                                "seriesValues": [round(one_quarter_utilised * 100, 2),
                                                 round(two_quarters_utilised * 100, 2),
                                                 round(three_quarters_utilised * 100, 2),
                                                 round(four_quarters_utilised * 100, 2)]
                            }
                        ]
                    }
            },
            {
                'type': "INFO",
                'data': "FILE"
            },
        ]
    }