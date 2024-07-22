import csv
import sys
import json
import configparser
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.deprecation import MiddlewareMixin
from csvvalidator import *
from scheduler.scheduler_alg.utils.constants import ColumnHeaders as ch
from scheduler.scheduler_alg.configuration import OptimizationConfiguration


class FileSecurityChecker(MiddlewareMixin):
    def process_request(self, request):
        dataset_code = request.POST.get("dataset_code")
        device_detail = request.FILES.get('device_detail')
        device_comfort = request.FILES.get('device_comfort')
        device_usage = request.FILES.get('device_usage')
        target_consumption = request.FILES.get('target_curve')
        configuration = request.FILES.get('configuration')

        isDatasetCodeValid = validateString(dataset_code, r"^[a-zA-Z0-9]{1,10}$")
        isDetailValid = validate(device_detail, build_details_file_validator, {"header": ch.DETAIL_FILE_HEADERS})
        isComfortValid = validate(device_comfort, build_hourly_information_validator,
                                  {"header": ch.HOURLY_INFORMATION_HEADER,
                                   "checkFunction": comfortValueInArray})
        isUsageValid = validate(device_usage, build_hourly_information_validator,
                                {"header": ch.HOURLY_INFORMATION_HEADER,
                                 "checkFunction": usageValueInArray})
        isTargetValid = validate(target_consumption, build_target_values_validator, {"header": ch.TARGET_CURVE_HEADERS,
                                                                                     "checkFunction": float})
        isConfigurationValid = validateProperties(configuration)

        print(f"isDatasetCodeValid = " + str(isDatasetCodeValid) + "\n isDetailValid = " + str(
            isDetailValid) + "\n isComfortValid = " + str(
            isComfortValid) + "\n isUsageValid = " + str(isUsageValid) + "\n isTargetConsumptionValid = " + str(
            isTargetValid) + "\n isConfigurationValid = " + str(isConfigurationValid))
        if not isDatasetCodeValid or not isDetailValid or not isComfortValid or not isUsageValid or not isTargetValid or not isConfigurationValid:
            return HttpResponse(json.dumps({'status': 'WRONG_FORMAT'}), content_type='application/json')


def validateProperties(file):
    if file is None:
        return True
    try:
        file_decoded = file.read().decode('utf-8').splitlines()
        config = configparser.ConfigParser()
        config.read_file(file_decoded)
        property_dict = dict(config.items('DEFAULT'))

        for param in OptimizationConfiguration.parameter_definitions:
            if param["paramName"] not in property_dict.keys():
                return False
            v = param["type"](property_dict[param["paramName"]])
        file.seek(0)
        return True
    except Exception as e:
        return False



def validateString(string, regex):
    if string is None:
        return True

    validator = RegexValidator(regex)
    try:
        validator(string)
        return True
    except ValidationError as e:
        return False

def validate(file_csv, validation_builder, arguments):
    if file_csv is None:
        return True
    try:
        file_decoded = file_csv.read().decode('utf-8').splitlines()
        isValid = is_valid_csv_file(validation_builder, file_decoded, arguments)
        file_csv.seek(0)
        return isValid
    except Exception as e:
        return False


def is_valid_csv_file(validator_function, file, arguments=None):
    validator = validator_function(arguments)
    fileReader = csv.reader(file)
    problems = validator.validate(fileReader)
    if len(problems) > 0:
        write_problems(problems, sys.stdout)
        return False
    return True


def build_details_file_validator(args=None):
    validator = CSVValidator(ch.DETAIL_FILE_HEADERS)
    validator.add_header_check("EX_H", "Wrong header number")
    validator.add_record_length_check("EX_R", "Wrong record number")

    validator.add_value_check(ch.APARTMENT_ID, int, "EX_V_I", "Wrong format apartment id")
    validator.add_value_check(ch.DEVICE_ID, int, "EX_V_I", "Wrong format device id")
    validator.add_value_check(ch.NAME, str, "EX_V_S", "Wrong format name")
    validator.add_value_check(ch.CONSUMPTION, float, "EX_V_F", "Wrong format consumption")
    validator.add_value_check(ch.IS_DEFERRABLE, detailValueInArray, "EX_V_B", "Wrong format is deferrable")
    validator.add_value_check(ch.MIN_USAGE_HOURS, int, "EX_V_I", "Wrong format min usage hours")

    return validator


def build_hourly_information_validator(configuration):
    validator = CSVValidator(configuration["header"])
    validator.add_header_check("EX_H", "Wrong header number")
    validator.add_record_length_check("EX_R", "Wrong record number")

    validator.add_value_check(ch.APARTMENT_ID, int, "EX_V_I", "Wrong format apartment id")
    validator.add_value_check(ch.DEVICE_ID, int, "EX_V_I", "Wrong format device id")

    add_hour_validators(validator, configuration)

    return validator


def build_target_values_validator(configuration):
    validator = CSVValidator(configuration["header"])
    validator.add_header_check("EX_H", "Wrong header number")
    validator.add_record_length_check("EX_R", "Wrong record number")

    add_hour_validators(validator, configuration)

    return validator


def add_hour_validators(validator, configuration):
    validator.add_value_check(ch.HOUR_0, configuration["checkFunction"], "EX_V_E", "Wrong format hour 0")
    validator.add_value_check(ch.HOUR_1, configuration["checkFunction"], "EX_V_E", "Wrong format hour 1")
    validator.add_value_check(ch.HOUR_2, configuration["checkFunction"], "EX_V_E", "Wrong format hour 2")
    validator.add_value_check(ch.HOUR_3, configuration["checkFunction"], "EX_V_E", "Wrong format hour 3")
    validator.add_value_check(ch.HOUR_4, configuration["checkFunction"], "EX_V_E", "Wrong format hour 4")
    validator.add_value_check(ch.HOUR_5, configuration["checkFunction"], "EX_V_E", "Wrong format hour 5")
    validator.add_value_check(ch.HOUR_6, configuration["checkFunction"], "EX_V_E", "Wrong format hour 6")
    validator.add_value_check(ch.HOUR_7, configuration["checkFunction"], "EX_V_E", "Wrong format hour 7")
    validator.add_value_check(ch.HOUR_8, configuration["checkFunction"], "EX_V_E", "Wrong format hour 8")
    validator.add_value_check(ch.HOUR_9, configuration["checkFunction"], "EX_V_E", "Wrong format hour 9")
    validator.add_value_check(ch.HOUR_10, configuration["checkFunction"], "EX_V_E", "Wrong format hour 10")
    validator.add_value_check(ch.HOUR_11, configuration["checkFunction"], "EX_V_E", "Wrong format hour 11")
    validator.add_value_check(ch.HOUR_12, configuration["checkFunction"], "EX_V_E", "Wrong format hour 12")
    validator.add_value_check(ch.HOUR_13, configuration["checkFunction"], "EX_V_E", "Wrong format hour 13")
    validator.add_value_check(ch.HOUR_14, configuration["checkFunction"], "EX_V_E", "Wrong format hour 14")
    validator.add_value_check(ch.HOUR_15, configuration["checkFunction"], "EX_V_E", "Wrong format hour 15")
    validator.add_value_check(ch.HOUR_16, configuration["checkFunction"], "EX_V_E", "Wrong format hour 16")
    validator.add_value_check(ch.HOUR_17, configuration["checkFunction"], "EX_V_E", "Wrong format hour 17")
    validator.add_value_check(ch.HOUR_18, configuration["checkFunction"], "EX_V_E", "Wrong format hour 18")
    validator.add_value_check(ch.HOUR_19, configuration["checkFunction"], "EX_V_E", "Wrong format hour 19")
    validator.add_value_check(ch.HOUR_20, configuration["checkFunction"], "EX_V_E", "Wrong format hour 20")
    validator.add_value_check(ch.HOUR_21, configuration["checkFunction"], "EX_V_E", "Wrong format hour 21")
    validator.add_value_check(ch.HOUR_22, configuration["checkFunction"], "EX_V_E", "Wrong format hour 22")
    validator.add_value_check(ch.HOUR_23, configuration["checkFunction"], "EX_V_E", "Wrong format hour 23")


def detailValueInArray(value):
    if int(value) not in [0, 1]:
        raise ValueError(f"Invalid detail value: {value}")


def comfortValueInArray(value):
    if int(value) not in ch.COMFORT_VALUES:
        raise ValueError(f"Invalid comfort value: {value}")


def usageValueInArray(value):
    if int(value) not in ch.USAGE_VALUES:
        raise ValueError(f"Invalid usage value: {value}")
