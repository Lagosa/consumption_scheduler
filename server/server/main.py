import numpy as np
import pandas as pd

from scheduler.scheduler_alg.configuration import InputConfiguration as InputConfiguration
from scheduler.scheduler_alg.data_model.DTO import BuildingConfiguration

from scheduler.scheduler_alg.utils.convertors import SystemInitilizer
from scheduler.scheduler_alg.chart_engine import EvaluationDiagrams
from scheduler.scheduler_alg.business_logic.schedule_providers import SubsetMaker, ScheduleMaker
from scheduler.scheduler_alg.business_logic.operations import ConsumptionOperations
from scheduler.scheduler_alg.configuration import OptimizationConfiguration
from scheduler.scheduler_alg.utils.constants import RunningModes
from scheduler.scheduler_alg.utils.generators import DatasetGenerator
from scheduler.scheduler_alg.business_logic.optimization_problem.GreedyOptimization import GreedyOptimization
from scheduler.scheduler_alg.module_operations import InitialConsumption


def main():
    OptimizationConfiguration.configureFromPath(InputConfiguration.input_folder_location + "/" + InputConfiguration.external_property_file_name)

    if OptimizationConfiguration.runtime_scenario == RunningModes.GENERATE_DATASET:
        building_device_info, building_comfort, building_usage = DatasetGenerator.generate_dataset(5, [0.5, 0.5])

        df = pd.DataFrame(building_device_info)
        df.columns = ["ap_id", "dev_id", "name", "consumption", "is_deferrable", "min_usage_hours"]
        df.to_csv(InputConfiguration.input_folder_location + "/" + InputConfiguration.input_detail_file + ".csv",
                  index=False)

        cols = ["ap_id", "dev_id", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
        df = pd.DataFrame(building_comfort)
        df.columns = cols
        df.to_csv(InputConfiguration.input_folder_location + "/" + InputConfiguration.input_comfort_file + ".csv",
                  index=False)

        df = pd.DataFrame(building_usage)
        df.columns = cols
        df.to_csv(InputConfiguration.input_folder_location + "/" + InputConfiguration.input_usage_file + ".csv",
                  index=False)

        return

    building_configuration = BuildingConfiguration.BuildingConfiguration(SystemInitilizer.initialize())
    target_consumption_df = SystemInitilizer.initialize_target_consumption()

    if OptimizationConfiguration.runtime_scenario == RunningModes.INITIAL_SCHEDULE_CONSUMPTION_VECTOR:
        print(InitialConsumption.do(building_configuration))
        return

    # Greedy approach only
    if OptimizationConfiguration.runtime_scenario == RunningModes.DO_GREEDY_OPTIMIZATION:
        initial_solution = np.zeros(building_configuration.usage_matrix.shape)
        greedy_optimization = GreedyOptimization(building_configuration, building_configuration.usage_matrix, target_consumption_df)
        greedy_optimization.solve(True)
        solution = greedy_optimization.solution
        EvaluationDiagrams.compareTotalConsumptionAndTarget(building_configuration.consumption_vector, solution, target_consumption_df)
        EvaluationDiagrams.drawComfortChart(solution, building_configuration.comfort_matrix)
        return

    if OptimizationConfiguration.runtime_scenario == RunningModes.COMPARE_INITIAL_AND_TARGET_CURVE:
        EvaluationDiagrams.compareTotalConsumptionAndTarget(building_configuration.consumption_vector,
                                                            building_configuration.usage_matrix, target_consumption_df)
        return

    if OptimizationConfiguration.runtime_scenario == RunningModes.COMPUTE_BASELINE_VALUES:
        baseline_comfort = ScheduleMaker.get_baseline_comfort_hourly(building_configuration, target_consumption_df)
        baseline_consumption = ScheduleMaker.get_baseline_consumption_hourly(building_configuration, target_consumption_df)

        print(f"Baseline consumption: {baseline_consumption}\nBaseline comfort: {baseline_comfort}")
        return

    if OptimizationConfiguration.runtime_scenario == RunningModes.DO_BI_LEVEL_OPTIMIZATION:
        subset, schedule, configuration, metrics, _ = SubsetMaker.do_subset(building_configuration, target_consumption_df)

        np.savetxt(InputConfiguration.input_folder_location + "/" + InputConfiguration.output_solution + ".csv",
                   schedule, delimiter=",")
        EvaluationDiagrams.compareTotalConsumptionAndTarget(configuration.consumption_vector, schedule,
                                                            target_consumption_df)
        EvaluationDiagrams.drawComfortChart(schedule, configuration.comfort_matrix)
        print(f"Included apartments in the DR program: {sum(subset)}")
        apartments_included = [ap_id + 1 for ap_id, is_included in enumerate(subset) if is_included == 1]
        print(f"Included apartments: {apartments_included}")
        return

    if OptimizationConfiguration.runtime_scenario == RunningModes.DO_FIRST_LEVEL_OPTIMIZATION:
        # best_solution_matrix_rounded, model, optimization_problem = ScheduleMaker.get_matrix_solution(
        #     building_configuration, target_consumption_df)

        best_solution_matrix_rounded = ScheduleMaker.get_matrix_solution(building_configuration, target_consumption_df)

        hourly_consumption_vector = ConsumptionOperations.compute_hourly_consumption(
            building_configuration.consumption_vector, best_solution_matrix_rounded)
        print(f"Resulting hourly consumption {hourly_consumption_vector}")
        np.savetxt(InputConfiguration.input_folder_location + "/" + InputConfiguration.output_solution + ".csv",
                   best_solution_matrix_rounded, delimiter=",")
        EvaluationDiagrams.compareTotalConsumptionAndTarget(building_configuration.consumption_vector,
                                                            best_solution_matrix_rounded, target_consumption_df)
        EvaluationDiagrams.drawComfortChart(best_solution_matrix_rounded, building_configuration.comfort_matrix)
        return


if __name__ == '__main__':
    main()
