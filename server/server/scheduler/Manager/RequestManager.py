from ..scheduler_alg.utils.convertors import SystemInitilizer
from scheduler.scheduler_alg.data_model.models.Dataset import Dataset
from django.db import IntegrityError
from django.db import transaction
from scheduler.scheduler_alg.module_operations import BaselineValues, CompareInitialAndTarget, FirstLevelOptimization, \
    InitialConsumption, BiLevelOptimization, GreedyOptimization
from scheduler.scheduler_alg.data_model.DTO import BuildingConfiguration
from ..scheduler_alg.configuration import OptimizationConfiguration

request_handler = {
    "INITIAL_CONSUMPTION": {'clazz': InitialConsumption, 'isTargetCurveRequired': False,
                            'isConfigurationRequired': False},
    "BASELINE_VALUES": {'clazz': BaselineValues, 'isTargetCurveRequired': True, 'isConfigurationRequired': True},
    "COMPARE_CURRENT_AND_TARGET_CURVE": {'clazz': CompareInitialAndTarget, 'isTargetCurveRequired': True,
                                         'isConfigurationRequired': False},
    "DO_FIRST_LEVEL_OPTIMIZATION": {'clazz': FirstLevelOptimization, 'isTargetCurveRequired': True,
                                    'isConfigurationRequired': True},
    "DO_GREEDY_OPTIMIZATION": {'clazz': GreedyOptimization, 'isTargetCurveRequired': True,
                               'isConfigurationRequired': True},
    "DO_BI_LEVEL_OPTIMIZATION": {'clazz': BiLevelOptimization, 'isTargetCurveRequired': True,
                                 'isConfigurationRequired': True},
    "REMOVE": {'clazz': None, 'isTargetCurveRequired': False, 'isConfigurationRequired': False},
}


@transaction.atomic()
def saveDataset(code, device_details_csv, comfort_definitions_csv, usage_definitions_csv):
    device_details_obj = SystemInitilizer.build_details_obj_from_file(device_details_csv)
    device_comfort_obj = SystemInitilizer.build_comfort_obj_from_file(comfort_definitions_csv)
    device_usage_obj = SystemInitilizer.build_usage_obj_from_file(usage_definitions_csv)

    try:
        dataset = Dataset(code)
        dataset.save(force_insert=True)
    except IntegrityError as e:
        print(f"Dataset code: {code} is taken!")
        return "TAKEN"

    associateDatasetWithDetails(dataset, device_details_obj, device_comfort_obj, device_usage_obj)
    dataset.save()
    return "OK"


def associateDatasetWithDetails(dataset, device_details, device_comfort, device_usage):
    for i in range(0, len(device_details)):
        device_details[i].save()
        device_comfort[i].save()
        device_usage[i].save()

        device_details[i].dataset = dataset
        device_comfort[i].dataset = dataset
        device_usage[i].dataset = dataset

        dataset.devicedetail_set.add(device_details[i])
        dataset.comfortdefinition_set.add(device_comfort[i])
        dataset.usagedefinition_set.add(device_usage[i])


def getDatasets():
    datasets = Dataset.objects.all().order_by("-code")
    return [dataset.code for dataset in datasets]


def handleRequest(operation_code, dataset_code, target_curve, configuration):
    dataset = Dataset.objects.filter(code=dataset_code).first()
    if dataset is None:
        return {'status': 'UNKNOWN_DATASET'}

    appliances = SystemInitilizer.initialize_objects(list(dataset.devicedetail_set.all()),
                                                     list(dataset.comfortdefinition_set.all()),
                                                     list(dataset.usagedefinition_set.all()))
    building_configuration = BuildingConfiguration.BuildingConfiguration(appliances)

    if operation_code not in request_handler.keys():
        return {'status': 'UNKNOWN_OPERATION'}

    if request_handler[operation_code]['isTargetCurveRequired'] and target_curve is None:
        return {'status': "INCOMPLETE"}

    if request_handler[operation_code]['isConfigurationRequired'] and configuration is None:
        return {'status': "INCOMPLETE"}
    else:
        if request_handler[operation_code]['isConfigurationRequired']:
            OptimizationConfiguration.configureFromFile(configuration)

    if operation_code == "REMOVE":
        return removeDataset(dataset_code)

    handler = request_handler[operation_code]['clazz']
    result = handler.do(building_configuration, target_curve)

    return result


def getOperationCodes():
    operation_code_list = []
    for opCode in request_handler.keys():
        operation_code_list.append(opCode)
    return operation_code_list


def removeDataset(datasetCode):
    dataset = Dataset.objects.get(code=datasetCode)
    dataset.delete()

    return {'status': "OPERATION_PERFORMED",
            'result': []}
