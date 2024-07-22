# transforms appliances given in the following form:
# [
#   {
#       apartment: 1
#       schedule {
#           0: 1,
#           1: 0,
#           2: 0,
#           3: 1,
#           .
#       }
#   },
#   {
#       apartment: 2
#       schedule {
#           0: 0,
#           1: 0,
#           2: 1,
#           3: 1,
#           .
#       }
#   }
# ]

# the resulting format is:
# {
#     (101,0): 1,
#     (101,1): 0,
#     (101,2): 0,
#     (101,3): 1,
#     (102,0): 0,
#     (102,1): 0,
#     (102,2): 1,
#     (102,3): 1,
#     .
# }

import utils.DeviceIdGenerator as IdGenerator


def transform(appliances):
    result = {}

    for appliance in appliances:
        id = IdGenerator.generateId(appliance.apartment, appliance.id)
        appliance_schedule = appliance.schedule

        for hour, state in appliance_schedule.items:
            result[(id, hour)] = state

    return result
