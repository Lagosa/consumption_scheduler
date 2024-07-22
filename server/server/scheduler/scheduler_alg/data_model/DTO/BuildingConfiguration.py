import numpy as np

class BuildingConfiguration:
    def __init__(self, appliances=None):
        if appliances is None:
            appliances = []

        sorted_appliances = sorted(appliances, key=lambda appliance: appliance.id)

        self.appliances = {}
        self.usage_matrix = []
        self.comfort_matrix = []
        self.consumption_vector = []
        self.constraint_matrix = np.zeros((len(appliances), 2))

        self.buildInternalRepresentation(sorted_appliances)

        self.usage_matrix = np.array(self.usage_matrix)
        self.comfort_matrix = np.array(self.comfort_matrix)
        self.consumption_vector = np.array(self.consumption_vector)

        self.no_apartments = count_apartments(self.appliances)

    def buildInternalRepresentation(self, appliances):

        for index, appliance in enumerate(appliances):
            self.appliances[appliance.id] = appliance

            appliance_usage = appliance.schedule_vector
            self.usage_matrix.append(appliance_usage)

            self.consumption_vector.append(appliance.consumption)

            appliance_comfort = appliance.comfort_vector
            self.comfort_matrix.append(appliance_comfort)

            is_deferrable = appliance.is_deferrable
            min_usage_hours = appliance.min_usage_hours
            self.constraint_matrix[index][0] = is_deferrable
            self.constraint_matrix[index][1] = min_usage_hours


def count_apartments(appliances):
    key_list = appliances.keys()
    ap_no_list = [ap for (ap, dev) in key_list]
    key_set = set(ap_no_list)

    return len(key_set)