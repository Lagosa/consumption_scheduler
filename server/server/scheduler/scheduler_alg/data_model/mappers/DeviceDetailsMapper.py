import csv

from ....scheduler_alg.data_model.models import DeviceDetails
from ...utils.constants import ColumnHeaders as ch


def build_definitions(device_details_csv):
    reader = csv.DictReader(device_details_csv)
    device_details = []
    for row in reader:
        device_details.append(
            DeviceDetails.DeviceDetail(-1, int(row[ch.APARTMENT_ID]), int(row[ch.DEVICE_ID]), row[ch.NAME], float(row[ch.CONSUMPTION]),
                                       int(row[ch.IS_DEFERRABLE]), int(row[ch.MIN_USAGE_HOURS])))
    return device_details