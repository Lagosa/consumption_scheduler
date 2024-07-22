import csv

from ....scheduler_alg.data_model.models.TargetConsumptions import TargetConsumption


def build(target_consumption_file):
    reader = csv.DictReader(target_consumption_file)
    
    row = next(reader)
    return TargetConsumption(float(row["0"]), float(row["1"]), float(row["2"]),
                             float(row["3"]), float(row["4"]), float(row["5"]),
                             float(row["6"]), float(row["7"]), float(row["8"]),
                             float(row["9"]), float(row["10"]), float(row["11"]),
                             float(row["12"]), float(row["13"]), float(row["14"]),
                             float(row["15"]), float(row["16"]), float(row["17"]),
                             float(row["18"]), float(row["19"]), float(row["20"]),
                             float(row["21"]), float(row["22"]), float(row["23"]))