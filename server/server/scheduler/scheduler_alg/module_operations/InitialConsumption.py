import numpy as np

from ...scheduler_alg.business_logic.operations import ConsumptionOperations


def do(building_configuration, target_curve):
    result = ConsumptionOperations.compute_hourly_consumption(building_configuration.consumption_vector,
                                                              building_configuration.usage_matrix)
    rounded_result = np.round(result, 2)
    return {
        'status': "OPERATION_PERFORMED",
        'result': [
            {
                'type': 'TABLE',
                'data':
                    {
                        'rows': [rounded_result],
                        'header': ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
                                   'H11', 'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20',
                                   'H21', 'H22', 'H23'],
                        'title': 'Initial consumption'
                    }
            }
        ]
    }
