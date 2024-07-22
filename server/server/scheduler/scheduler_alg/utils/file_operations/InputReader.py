import numpy as np
from ...utils.constants import ColumnHeaders as ch


def load_appliance_detail_obj(deviceDetails):
    appliance_details = []

    for deviceDetail in deviceDetails:
        appliance_details.append({'apartment_id': deviceDetail.ap_id,
                                  'appliance_id': deviceDetail.dev_id,
                                  "name": deviceDetail.name,
                                  "consumption": deviceDetail.consumption,
                                  'is_deferrable': deviceDetail.is_deferrable,
                                  'min_usage_hours': deviceDetail.min_usage_hours})

    return appliance_details

def load_appliance_comfort_info_obj(comfortDefinitions):
    comfort_info = {}

    for comfort in comfortDefinitions:
        row_id = get_row_identifier(comfort.ap_id, comfort.dev_id)

        comfort_info[row_id] = np.array([comfort.h0, comfort.h1, comfort.h2, comfort.h3, comfort.h4, comfort.h5, comfort.h6,
                                comfort.h7, comfort.h8, comfort.h9, comfort.h10, comfort.h11, comfort.h12, comfort.h13,
                                comfort.h14, comfort.h15, comfort.h16, comfort.h17, comfort.h18, comfort.h19, comfort.h20,
                                comfort.h21, comfort.h22, comfort.h23])

    return comfort_info


def load_appliance_usage_info_obj(usageDefinitions):
    usage_info = {}

    for usage in usageDefinitions:
        row_id = get_row_identifier(usage.ap_id, usage.dev_id)

        usage_info[row_id] = np.array([usage.h0, usage.h1, usage.h2, usage.h3, usage.h4, usage.h5, usage.h6,
                                usage.h7, usage.h8, usage.h9, usage.h10, usage.h11, usage.h12, usage.h13,
                                usage.h14, usage.h15, usage.h16, usage.h17, usage.h18, usage.h19,
                                usage.h20,
                                usage.h21, usage.h22, usage.h23])

    return usage_info



def load_appliance_detail(fileName):
    appliance_detail_df = load_file(fileName)
    appliances_details = []

    for index, row in appliance_detail_df.iterrows():
        appliance_detail = extract_appliance_detail_information(row)
        appliances_details.append(appliance_detail)

    return appliances_details


def load_appliance_hourly_info(filename):
    appliance_hourly_info_df = load_file(filename)
    appliances_hourly_info = {}

    for index, row in appliance_hourly_info_df.iterrows():
        appliance_hourly_info = extract_hourly_information(row)

        row_id = get_row_identifier_row(row, ch.APARTMENT_ID, ch.DEVICE_ID)
        appliances_hourly_info[row_id] = appliance_hourly_info

    return appliances_hourly_info


def load_file(filename):
    appliance_info_df = open(filename, 'r')
    return appliance_info_df


def extract_appliance_detail_information(appliancerow):
    apartment_id = appliancerow[ch.APARTMENT_ID]
    appliance_id = appliancerow[ch.DEVICE_ID]
    name = appliancerow[ch.NAME]
    consumption = appliancerow[ch.CONSUMPTION]
    is_deferrable = appliancerow[ch.IS_DEFERRABLE]
    min_usage_hours = appliancerow[ch.MIN_USAGE_HOURS]

    return {'apartment_id': apartment_id, 'appliance_id': appliance_id, "name": name, "consumption": consumption,
            'is_deferrable': is_deferrable, 'min_usage_hours': min_usage_hours}


def extract_hourly_information(appliancerow):
    h0 = appliancerow[ch.HOUR_0]
    h1 = appliancerow[ch.HOUR_1]
    h2 = appliancerow[ch.HOUR_2]
    h3 = appliancerow[ch.HOUR_3]
    h4 = appliancerow[ch.HOUR_4]
    h5 = appliancerow[ch.HOUR_5]
    h6 = appliancerow[ch.HOUR_6]
    h7 = appliancerow[ch.HOUR_7]
    h8 = appliancerow[ch.HOUR_8]
    h9 = appliancerow[ch.HOUR_9]
    h10 = appliancerow[ch.HOUR_10]
    h11 = appliancerow[ch.HOUR_11]
    h12 = appliancerow[ch.HOUR_12]
    h13 = appliancerow[ch.HOUR_13]
    h14 = appliancerow[ch.HOUR_14]
    h15 = appliancerow[ch.HOUR_15]
    h16 = appliancerow[ch.HOUR_16]
    h17 = appliancerow[ch.HOUR_17]
    h18 = appliancerow[ch.HOUR_18]
    h19 = appliancerow[ch.HOUR_19]
    h20 = appliancerow[ch.HOUR_20]
    h21 = appliancerow[ch.HOUR_21]
    h22 = appliancerow[ch.HOUR_22]
    h23 = appliancerow[ch.HOUR_23]

    hours = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16, h17, h18, h19, h20, h21, h22,
             h23]
    return hours


def get_row_identifier_row(row, col1, col2):
    return (row[col1], row[col2])

def get_row_identifier(ap_id, dev_id):
    return (int(ap_id), int(dev_id))
