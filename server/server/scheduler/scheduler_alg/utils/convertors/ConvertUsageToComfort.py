from ....scheduler_alg.utils.file_operations import InputReader as InputReader
from ....scheduler_alg.configuration import InputConfiguration
from ....scheduler_alg.utils.constants import ColumnHeaders as ch
import numpy as np


def loadDataFrame(fileName):
    device_usage_df = InputReader.load_file(fileName)

    return device_usage_df


def replaceUsageValues(device_usage_df, to_be_replaced, replacement, cols_to_exclude):
    cols_to_replace_in = device_usage_df.columns.difference(cols_to_exclude)

    device_usage_df[cols_to_replace_in] = np.where(device_usage_df[cols_to_replace_in] == to_be_replaced, replacement,
                                                   device_usage_df[cols_to_replace_in])

    return device_usage_df


if __name__ == '__main__':
    folder = InputConfiguration.input_folder_location
    file = InputConfiguration.input_usage_file

    usage_df = loadDataFrame(folder + "/" + file + ".csv")

    replaced_df = replaceUsageValues(usage_df, 0, 2, [ch.APARTMENT_ID, ch.DEVICE_ID])
    replaced_df = replaceUsageValues(replaced_df, 1, 0, [ch.APARTMENT_ID, ch.DEVICE_ID])

    replaced_df.to_csv(folder + "/" + file + "_replaced.csv", index=False)
