import csv
from ...utils.constants import ColumnHeaders as ch


def build_definitions(clazz, comfort_definitions_csv):
    reader = csv.DictReader(comfort_definitions_csv)

    hourly_information = []
    for row in reader:
        hourly_information.append(
            clazz(-1, int(row[ch.APARTMENT_ID]), int(row[ch.DEVICE_ID]), int(row[ch.HOUR_0]), int(row[ch.HOUR_1]),
                  int(row[ch.HOUR_2]), int(row[ch.HOUR_3]),
                  int(row[ch.HOUR_4]), int(row[ch.HOUR_5]), int(row[ch.HOUR_6]), int(row[ch.HOUR_7]),
                  int(row[ch.HOUR_8]), int(row[ch.HOUR_9]), int(row[ch.HOUR_10]),
                  int(row[ch.HOUR_11]), int(row[ch.HOUR_12]), int(row[ch.HOUR_13]), int(row[ch.HOUR_14]),
                  int(row[ch.HOUR_15]), int(row[ch.HOUR_16]), int(row[ch.HOUR_17]),
                  int(row[ch.HOUR_18]), int(row[ch.HOUR_19]), int(row[ch.HOUR_20]), int(row[ch.HOUR_21]),
                  int(row[ch.HOUR_22]), int(row[ch.HOUR_23])))

    return hourly_information
