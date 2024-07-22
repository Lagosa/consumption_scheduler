import numpy as np

from ....scheduler_alg.utils.file_operations import InputReader
from ....scheduler_alg.configuration import InputConfiguration
from ....scheduler_alg.data_model.DTO import Appliance
from ....scheduler_alg.data_model.mappers import TargetConsumptionMapper, HourlyInformationMapper, \
    DeviceDetailsMapper
from ....scheduler_alg.data_model.models.ComfortDefinitions import ComfortDefinition
from ....scheduler_alg.data_model.models.UsageDefinitions import UsageDefinition


def initialize_target_consumption():
    target_consumption = load_target_consumption()

    return initialize_target_consumption_file(target_consumption)


def initialize_target_consumption_file(target_consumption_file):
    target_consumption = TargetConsumptionMapper.build(target_consumption_file)
    return initialize_target_consumption_obj(target_consumption)


def initialize_target_consumption_obj(target_consumption):
    return np.array([target_consumption.h0, target_consumption.h1, target_consumption.h2, target_consumption.h3,
                     target_consumption.h4, target_consumption.h5, target_consumption.h6, target_consumption.h7,
                     target_consumption.h8, target_consumption.h9, target_consumption.h10, target_consumption.h11,
                     target_consumption.h12, target_consumption.h13, target_consumption.h14, target_consumption.h15,
                     target_consumption.h16, target_consumption.h17, target_consumption.h18, target_consumption.h19,
                     target_consumption.h20, target_consumption.h21, target_consumption.h22, target_consumption.h23])


def initialize():
    appliances_detail_csv = load_appliance_detail()
    appliances_usage_csv = load_appliance_usage()
    appliances_comfort_csv = load_appliance_comfort()

    configuration = initialize_files(appliances_detail_csv, appliances_usage_csv, appliances_comfort_csv)

    return configuration


def initialize_files(device_details_csv, comfort_csv, usage_csv):
    device_information = build_details_obj_from_file(device_details_csv)
    comfort_definitions = build_comfort_obj_from_file(comfort_csv)
    usage_definitions = build_usage_obj_from_file(usage_csv)

    return initialize_objects(device_information, comfort_definitions, usage_definitions)


def build_details_obj_from_file(device_details_csv):
    return DeviceDetailsMapper.build_definitions(device_details_csv)


def build_comfort_obj_from_file(device_comfort_csv):
    return HourlyInformationMapper.build_definitions(ComfortDefinition, device_comfort_csv)


def build_usage_obj_from_file(device_usage_csv):
    return HourlyInformationMapper.build_definitions(UsageDefinition,device_usage_csv)


def initialize_objects(device_details_obj, comfort_obj, usage_obj):
    appliances_detail = InputReader.load_appliance_detail_obj(device_details_obj)
    appliances_comfort = InputReader.load_appliance_usage_info_obj(comfort_obj)
    appliances_usage = InputReader.load_appliance_comfort_info_obj(usage_obj)

    configuration = build_initial_configuration(appliances_detail, appliances_usage, appliances_comfort)

    return configuration


def load_target_consumption():
    target_consumption_path = InputConfiguration.input_folder_location + "/" + InputConfiguration.input_target_file + ".csv"
    target_consumption_file = InputReader.load_file(target_consumption_path)

    return target_consumption_file


def load_appliance_detail():
    detail_file = InputConfiguration.input_folder_location + "/" + InputConfiguration.input_detail_file + ".csv"
    appliance_detail_df = InputReader.load_file(detail_file)

    return appliance_detail_df


def load_appliance_usage():
    usage_file = InputConfiguration.input_folder_location + "/" + InputConfiguration.input_usage_file + ".csv"
    appliances_usage = InputReader.load_file(usage_file)

    return appliances_usage


def load_appliance_comfort():
    comfort_file = InputConfiguration.input_folder_location + "/" + InputConfiguration.input_comfort_file + ".csv"
    appliances_comfort = InputReader.load_file(comfort_file)

    return appliances_comfort


def build_initial_configuration(appliances_detail, appliances_usage, appliances_comfort):
    building_configuration = []

    for appliance in appliances_detail:
        schedule = get_schedule_of_appliance(appliance, appliances_usage)
        comfort = get_comfort_of_appliance(appliance, appliances_comfort)

        appliance_instance = create_appliance(appliance, schedule, comfort)

        building_configuration.append(appliance_instance)

    return building_configuration


def create_appliance(appliance, schedule, comfort):
    appliance_instance = create_appliance_instance(appliance)
    appliance_instance.schedule_vector = schedule
    appliance_instance.comfort_vector = comfort

    return appliance_instance


def create_appliance_instance(appliance):
    apartment_id = appliance["apartment_id"]
    appliance_id = appliance["appliance_id"]
    name = appliance["name"]
    consumption = appliance["consumption"]
    is_deferrable = appliance["is_deferrable"]
    min_usage_hours = appliance["min_usage_hours"]

    return Appliance.Appliance(apartment_id, appliance_id, name, name, consumption, is_deferrable, min_usage_hours)


def get_schedule_of_appliance(appliance, appliances_usage):
    row_id = InputReader.get_row_identifier_row(appliance, "apartment_id", "appliance_id")
    return appliances_usage[row_id]


def get_comfort_of_appliance(appliance, appliances_comfort):
    row_id = InputReader.get_row_identifier_row(appliance, "apartment_id", "appliance_id")
    return appliances_comfort[row_id]
