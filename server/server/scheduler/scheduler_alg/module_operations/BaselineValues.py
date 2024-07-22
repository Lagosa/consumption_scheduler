from ...scheduler_alg.business_logic.schedule_providers import ScheduleMaker


def do(building_configuration, target_consumption):
    baseline_comfort = ScheduleMaker.get_baseline_comfort_hourly(building_configuration, target_consumption)
    baseline_consumption = ScheduleMaker.get_baseline_consumption_hourly(building_configuration, target_consumption)

    baseline_comfort_rounded = round(baseline_comfort, 2)
    baseline_consumption_rounded = round(baseline_consumption, 2)

    return {
        'status': "OPERATION_PERFORMED",
        'result': [
            {
                'type': "TABLE",
                'data':
                    {
                        'rows': [["Comfort baseline:", baseline_comfort_rounded], ["Consumption baseline:", baseline_consumption_rounded]],
                        'header': [],
                        'title': "Baseline values"
                    }
            }
        ]
    }
