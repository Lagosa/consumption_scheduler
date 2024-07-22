import configparser


comfort_penalty_base = 0
schedule_epoch_no = 0
schedule_population_size = 0
comfort_tradeoff = 0.0
comfort_weight = 0.0
approximation_weight = 0.0
over_sampling_weight = 0.0
subset_weight = 0.0
discrete_transform_threshold = 0.0
fitness_reference_value = 0
subset_epoch_number = 0
subset_population_size = 0
subset_crossover_probability = 0.0
subset_mutation_probability = 0.0
runtime_scenario = ""
baseline_consumption_euclidean = 0
baseline_consumption_pearson = 0
baseline_comfort = 0
should_adjust_fitness = 0
weight_euclidean_obj_metric = 0.0
weight_pearson_obj_metric = 0.0
first_level_no_processes = 1
first_level_no_iterations = 1
upper_level_no_processes = 1
apply_min_usage_hour_constraint = 1


default_values = {
    "comfort_penalty_base": 1.1,
    "schedule_epoch_no": 200,
    "schedule_population_size": 200,
    "comfort_tradeoff": 1.1,
    "comfort_weight": 1.1,
    "approximation_weight": 1.1,
    "discrete_transform_threshold": 0.5,
    "fitness_reference_value": 500,
    "over_sampling_weight": 0.5,
    "subset_weight": 0.5,
    "subset_epoch_number": 40,
    "subset_population_size": 40,
    "subset_mutation_probability": 0.01,
    "subset_crossover_probability": 0.8,
    "runtime_scenario": "INITIAL_SCHEDULE_CONSUMPTION_VECTOR",
    "baseline_consumption_euclidean": 1177,
    "baseline_consumption_pearson": 1,
    "baseline_comfort": 2334,
    "should_adjust_fitness": 1,
    "weight_euclidean_obj_metric": 0.5,
    "weight_pearson_obj_metric": 0.5,
    "first_level_no_processes": 1,
    "first_level_no_iterations": 1,
    "upper_level_no_processes": 1,
    "apply_min_usage_hour_constraint": 1,
}

parameter_definitions = [
    {"paramName": "comfort_penalty_base", "type": float},
    {"paramName": "schedule_epoch_no", "type": int},
    {"paramName": "schedule_population_size", "type": int},
    {"paramName": "comfort_tradeoff", "type": float},
    {"paramName": "comfort_weight", "type": float},
    {"paramName": "approximation_weight", "type": float},
    {"paramName": "over_sampling_weight", "type": float},
    {"paramName": "subset_weight", "type": float},
    {"paramName": "discrete_transform_threshold", "type": float},
    {"paramName": "fitness_reference_value", "type": int},
    {"paramName": "subset_epoch_number", "type": int},
    {"paramName": "subset_population_size", "type": int},
    {"paramName": "subset_crossover_probability", "type": float},
    {"paramName": "subset_mutation_probability", "type": float},
    {"paramName": "runtime_scenario", "type": str},
    {"paramName": "baseline_consumption_euclidean", "type": int},
    {"paramName": "baseline_consumption_pearson", "type": int},
    {"paramName": "baseline_comfort", "type": int},
    {"paramName": "should_adjust_fitness", "type": int},
    {"paramName": "weight_euclidean_obj_metric", "type": float},
    {"paramName": "weight_pearson_obj_metric", "type": float},
    {"paramName": "first_level_no_processes", "type": int},
    {"paramName": "first_level_no_iterations", "type": int},
    {"paramName": "upper_level_no_processes", "type": int},
    {"paramName": "apply_min_usage_hour_constraint", "type": int},
]


def configureFromPath(filePath):
    file = open(filePath)
    configureFromFile(file)


def configureFromFile(file):
    configuration_file = parse_configuration_file(file)
    setValues(configuration_file)


def parse_configuration_file(file):
    config = configparser.ConfigParser()
    try:
        config.read_file(file)
        return dict(config.items('DEFAULT'))
    except FileNotFoundError:
        return default_values


def setValues(property_file):
    global comfort_penalty_base
    comfort_penalty_base = float(property_file["comfort_penalty_base"])
    global schedule_epoch_no
    schedule_epoch_no = int(property_file["schedule_epoch_no"])
    global schedule_population_size
    schedule_population_size = int(property_file["schedule_population_size"])
    global comfort_tradeoff
    comfort_tradeoff = float(property_file["comfort_tradeoff"])
    global comfort_weight
    comfort_weight = float(property_file["comfort_weight"])
    global approximation_weight
    approximation_weight = float(property_file["approximation_weight"])
    global over_sampling_weight
    over_sampling_weight = float(property_file["over_sampling_weight"])
    global subset_weight
    subset_weight = float(property_file["subset_weight"])
    global discrete_transform_threshold
    discrete_transform_threshold = float(property_file["discrete_transform_threshold"])
    global fitness_reference_value
    fitness_reference_value = int(property_file["fitness_reference_value"])
    global subset_epoch_number
    subset_epoch_number = int(property_file["subset_epoch_number"])
    global subset_population_size
    subset_population_size = int(property_file["subset_population_size"])
    global subset_crossover_probability
    subset_crossover_probability = float(property_file["subset_crossover_probability"])
    global subset_mutation_probability
    subset_mutation_probability = float(property_file["subset_mutation_probability"])
    global runtime_scenario
    runtime_scenario = property_file["runtime_scenario"]
    global baseline_consumption_euclidean
    baseline_consumption_euclidean = int(property_file["baseline_consumption_euclidean"])
    global baseline_consumption_pearson
    baseline_consumption_pearson = int(property_file["baseline_consumption_pearson"])
    global baseline_comfort
    baseline_comfort = int(property_file["baseline_comfort"])
    global should_adjust_fitness
    should_adjust_fitness = int(property_file["should_adjust_fitness"])
    global weight_euclidean_obj_metric
    weight_euclidean_obj_metric = float(property_file["weight_euclidean_obj_metric"])
    global weight_pearson_obj_metric
    weight_pearson_obj_metric = float(property_file["weight_pearson_obj_metric"])
    global first_level_no_processes
    first_level_no_processes = int(property_file["first_level_no_processes"])
    global first_level_no_iterations
    first_level_no_iterations = int(property_file["first_level_no_iterations"])
    global upper_level_no_processes
    upper_level_no_processes = int(property_file["upper_level_no_processes"])
    global apply_min_usage_hour_constraint
    apply_min_usage_hour_constraint = int(property_file["apply_min_usage_hour_constraint"])
