def get_appliances_according_to_subset(bitstring, building_configuration):
    appliances = []

    non_selected_consumption = [0 for _ in range(0, 24)]
    for id, appliance in building_configuration.appliances.items():
        apartment = id[0]
        if bitstring[apartment] == 1:
            appliances.append(appliance)
        else:
            for hour in range(0, 24):
                non_selected_consumption[hour] += appliance.schedule_vector[hour] * appliance.consumption

    return appliances, non_selected_consumption
