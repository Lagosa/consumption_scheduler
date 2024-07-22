
class Appliance:
    id = (0,0)
    name = ""
    type = ""
    consumption = 0
    comfort_vector = []
    schedule_vector = []
    is_deferrable = False
    min_usage_hours = 0


    def __init__(self, apartment, appliance_number, name, type, consumption, is_deferrable, min_usage_hours,
                 comfort_vector=None, schedule_vector=None):
        self.id = (apartment, appliance_number)
        self.name = name
        self.type = type
        self.consumption = consumption
        self.comfort_vector = comfort_vector
        self.schedule_vector = schedule_vector
        self.is_deferrable = is_deferrable
        self.min_usage_hours = min_usage_hours

    def get_consumption(self):
        return self.consumption

    def is_over_minimum_usage(self, usage):
        return self.minimum_usage_time <= usage
