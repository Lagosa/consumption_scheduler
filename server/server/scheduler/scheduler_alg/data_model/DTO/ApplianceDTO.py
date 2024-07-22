
valid_timeframe = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

class ApplianceDTO:

    id = 0
    apartment = 0
    name = ""
    consumption = 0
    minimum_usage_time = 0
    schedule = {}
    comfort_vector = {}

    def __init__(self, apartment, id, name, consumption, minimum_usage_time, schedule, comfort_vector):
        if not self.is_timeframe_integrous(schedule):
            raise Exception("Schedule vector integrity check failed")
        if not self.is_timeframe_integrous(comfort_vector):
            raise Exception("Comfort vector integrity check failed")

        self.apartment = apartment
        self.id = id
        self.name = name
        self.consumption = consumption
        self.minimum_usage_time = minimum_usage_time
        self.schedule = schedule
        self.comfort_vector = comfort_vector
        
    def is_timeframe_integrous(self, timeframe):
        defined_time_entries = list(timeframe.keys())
        return valid_timeframe == defined_time_entries
