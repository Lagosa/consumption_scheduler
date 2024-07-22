import numpy as np

from ...scheduler_alg.business_logic.operations import ConsumptionOperations


def do(building_configuration, target_curve):
    hourly_total_consumption = ConsumptionOperations.compute_hourly_consumption(
        building_configuration.consumption_vector, building_configuration.usage_matrix)

    rounded_hourly_total_consumption = np.round(hourly_total_consumption, 2)
    label = np.array(range(0, 24))
    return {
        'status': "OPERATION_PERFORMED",
        'result': [
            {
                'type': "CHART",
                'data':
                    {
                        'label': label,
                        'yAxisTitle': 'Consumption (kWh)',
                        'xAxisTitle': 'Hour',
                        'type': 'LINE',
                        'title': 'Current consumption vs. Target consumption',
                        'valuesArray':
                            [
                                {
                                    'seriesName': 'Current consumption',
                                    'seriesValues': rounded_hourly_total_consumption
                                },
                                {
                                    'seriesName': 'Target consumption',
                                    'seriesValues': np.array(target_curve)
                                }
                            ]
                    }
            }
        ]
    }
