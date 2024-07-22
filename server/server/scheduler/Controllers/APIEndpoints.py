from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..scheduler_alg.utils.convertors import SystemInitilizer
from scheduler.scheduler_alg.module_operations import InitialConsumption
from scheduler.scheduler_alg.data_model.DTO import BuildingConfiguration
from ..Manager import RequestManager
from django.http import HttpResponse
from ..scheduler_alg.configuration import InputConfiguration


@api_view(['GET'])
def getData(request):
    print(f"Got request: {request}")
    return Response({'MyResponse': 'Hello!'})

@api_view(['GET'])
def get_datasets(request):
    datasets = RequestManager.getDatasets()

    return Response(datasets)

@api_view(['GET'])
def get_operationCodes(request):
    operationCodes = RequestManager.getOperationCodes()
    return Response(operationCodes)

@api_view(['GET'])
def get_solutionFile(request):
    file_content = None
    with open(InputConfiguration.output_location + "/" + InputConfiguration.output_solution + ".csv", 'r') as file:
        file_content = file.read()

    response = HttpResponse(file_content, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Solution_schedule.csv"'

    return response

@api_view(['POST'])
def save_dataset(request):
    dataset_code = request.POST.get("dataset_code")
    device_detail = request.FILES.get('device_detail')
    device_comfort = request.FILES.get('device_comfort')
    device_usage = request.FILES.get('device_usage')



    if dataset_code is None or device_detail is None or device_comfort is None or device_usage is None:
        print("Incomplete: "
              "code=" + ("None" if dataset_code is None else dataset_code.name) +
              " detail=" + ("None" if device_detail is None else device_detail.name) +
              " comfort=" + ("None" if device_comfort is None else device_comfort.name) +
              " usage="+("None" if device_usage is None else device_usage.name))
        return Response({'status': "INCOMPLETE"})

    decoded_file_device_detail = device_detail.read().decode('utf-8').splitlines()
    decoded_file_device_comfort = device_comfort.read().decode('utf-8').splitlines()
    decoded_file_device_usage = device_usage.read().decode('utf-8').splitlines()

    status = RequestManager.saveDataset(dataset_code, decoded_file_device_detail, decoded_file_device_comfort,
                                        decoded_file_device_usage)

    return Response({'status': status})

@api_view(['POST'])
def initial_consumption(request):
    building_configuration, _ = parseFilesFromRequest(request)
    initialConsumption = InitialConsumption.do(building_configuration)

    return Response({'status': initialConsumption})

@api_view(['POST'])
def evaluate(request):
    operation_code = request.POST.get("operation_code")
    dataset_code = request.POST.get("dataset_code")
    target_curve = request.FILES.get("target_curve")
    configuration = request.FILES.get("configuration")

    target_curve_obj = None
    if target_curve is not None:
        decoded_file_target_curve = target_curve.read().decode('utf-8').splitlines()
        target_curve_obj = SystemInitilizer.initialize_target_consumption_file(decoded_file_target_curve)

    configuration_decoded = None
    if configuration is not None:
        configuration_decoded = configuration.read().decode('utf-8').splitlines()

    if operation_code is None:
        return Response({'status': 'INCOMPLETE'})

    result = RequestManager.handleRequest(operation_code, dataset_code, target_curve_obj, configuration_decoded)
    return Response(result)

def parseFilesFromRequest(request):
    device_detail = request.FILES['device_detail']
    device_comfort = request.FILES['device_comfort']
    device_usage = request.FILES['device_usage']
    target_consumption_file = request.FILES['target_consumption']

    decoded_file_device_detail = device_detail.read().decode('utf-8').splitlines()
    decoded_file_device_comfort = device_comfort.read().decode('utf-8').splitlines()
    decoded_file_device_usage = device_usage.read().decode('utf-8').splitlines()

    appliances = SystemInitilizer.initialize_files(decoded_file_device_detail, decoded_file_device_comfort,
                                                   decoded_file_device_usage)
    building_configuration = BuildingConfiguration.BuildingConfiguration(appliances)

    target_consumption = None
    if target_consumption_file is not None:
        decoded_target_consumption = target_consumption_file.read().decode('utf-8').splitlines()
        target_consumption = SystemInitilizer.initialize_target_consumption_file(decoded_target_consumption)

    return building_configuration, target_consumption
