import configparser

def get_config():
    try:
        parser = configparser.ConfigParser()
        parser.read_file(open("./input_location.txt"))
        return dict(parser.items("DEFAULT"))
    except FileNotFoundError:
        print("Could not locate configuration file!\n Move sample file out of the sample_input_config folder one level above.")

input_config = get_config()

input_folder_location = input_config["location"]
output_location = input_config["output_location"]

input_detail_file = input_config["device_info_file"]
input_usage_file = input_config["device_usage_file"]
input_comfort_file = input_config["comfort_file"]
input_target_file = input_config["target_consumption_file"]

output_solution = input_config["solution_file"]

external_property_file_name = input_config["optimization_config_file"]


