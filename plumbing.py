import math
import numpy as np

# @ water_pipe

import math
def select_pipe_material(year):
    if year < 1970:
        return "galvanized steel", 7850 # density in kg/m^3
    elif year < 2000:
        return "copper", 8960
    else:
        return "pex", 940
    
def decide_pipe_size(material):    
    # Assume typical dimensions for the selected material
    if material == "copper":
        diameter = 2.54  # in cm
        wall_thickness = 0.165  # in cm
    elif material == "pex":
        diameter = 1.6  # in cm
        wall_thickness = 0.2  # in cm
    elif material == "galvanized steel":
        diameter = 2.54  # in cm
        wall_thickness = 0.15  # in cm
        return diameter, wall_thickness
    
# assuming duct length in each room is half perimeter of the rooms with water supply 
# assuming distance from main water supply pipe to the furthest room is half perimeter of the building
def calculate_water_pipe_length_per_apartment(num_rooms, num_kitchens,living_space):

    a = 2 # assume 1 bathroom per 2 rooms
    num_bathrooms = num_rooms/a
    # assuming water pipe length in each room is half perimeter of the room
    water_pipe_length_per_floor_per_apartment= ((num_bathrooms + num_kitchens) * (living_space**0.5)) * 2 

    return water_pipe_length_per_floor_per_apartment

def calculate_water_pipe_length_building(total_length_apartment, num_floors, floor_height, building_area):
    # assuming water pipe uniform for now
    buffer = 0.15 # Fitting Factor (typically 0.10 to 0.15 for 10-15% additional length)
    water_pipe_length = (total_length_apartment + floor_height * num_floors * 2 + (building_area**0.5)*2) * (1 + buffer)

    return water_pipe_length

def pipe_size_cm(residents_per_floor, number_of_floors):
    # Define pipe sizes in centimeters
    pipe_sizes_cm = {
        "small": {
            (1, 4): 1.27,   # 1/2 inch
            (5, 8): 1.91,   # 3/4 inch
            (9, 12): 2.54   # 1 inch
        },
        "medium": {
            (1, 4): 1.91,   # 3/4 inch
            (5, 8): 2.54,   # 1 inch
            (9, 12): 3.18,  # 1 1/4 inch
            (13, 16): 3.81  # 1 1/2 inch
        },
        "large": {
            (1, 4): 2.54,   # 1 inch
            (5, 8): 3.18,   # 1 1/4 inch
            (9, 12): 3.81,  # 1 1/2 inch
            (13, 16): 5.08  # 2 inch
        }
    }
    
    # Determine building type based on number of floors
    if number_of_floors <= 3:
        building_type = "small"
    elif 4 <= number_of_floors <= 10:
        building_type = "medium"
    else:
        building_type = "large"
    
    # Determine the pipe size in centimeters based on the number of residents per floor
    pipe_size_cm = None
    for (min_res, max_res), size in pipe_sizes_cm[building_type].items():
        if min_res <= residents_per_floor <= max_res:
            pipe_size_cm = size
            break
    
    if pipe_size_cm is not None:
        return pipe_size_cm
    else:
        return 2.54


def calculate_water_pipe_weight(pipe_length, density, diameter, wall_thickness):
    inner_diameter = diameter - 2 * wall_thickness
    volume_per_meter = math.pi / 4 * (diameter**2 - inner_diameter**2)/1e4
    weight_per_meter = volume_per_meter * density
    total_weight = pipe_length * weight_per_meter
    return total_weight


def estimate_water_pipe_materials(weight, pipe_type):
    material_pct = {}
    
    if pipe_type == "copper":
        material_pct = {'copper': 1.00}
    elif pipe_type == "pvc":
        material_pct = {'pvc': 1.00}
    elif pipe_type == "cpvc":
        material_pct = {'cpvc': 1.00}
    elif pipe_type == "pex":
        material_pct = {'pex': 1.00}
    elif pipe_type == "galvanized steel":
        material_pct = {'steel': 0.99, 'zinc coating': 0.01}
    elif pipe_type == "mlc":
        material_pct = {'plastic': 0.60, 'aluminum': 0.40}
    
    material_weights = {material: weight * pct for material, pct in material_pct.items()}
    return material_weights


# @ water boiler
# assumimg a mean daily consumption of approximately 50 l/person at a DHW set-point temperature (tdhw-set) of 40, 45, 50 and 60 °C was considered
# https://www.sciencedirect.com/science/article/pii/B9780128042205000072
def dhw_boiler_capacity_kw(total_num_residents):
    dhw_capacity = total_num_residents * 50  # liters/day
    dhw_boiler_capacity_kw = dhw_capacity * 4.2 * (90-20) / 3600 / 0.9 # kWh/day, assuming 90% efficiency
    dhw_boiler_capacity_kw = dhw_boiler_capacity_kw / 24 # kW
    return dhw_boiler_capacity_kw

# @ plumbing fixtures
# assuming 1 toilet, 1 shower, 1 sink, 1 bathtub per bathroom
# assuming 1 bathroom per 2 rooms
def calculate_num_bathroom(num_rooms):
    a = 2 # assume 1 bathroom per 2 rooms
    num_bathrooms = np.floor(num_rooms/a)
    return num_bathrooms

import numpy as np

def calculate_num_bathroom(num_rooms):
    """
    Calculate the number of bathrooms based on the number of rooms.

    Parameters:
    num_rooms (int): Number of rooms.

    Returns:
    int: Number of bathrooms.
    """
    num_bathrooms = np.floor(num_rooms / 2)
    return int(num_bathrooms)


def estimate_toilet_materials(num_toilets, weight_per_toilet):
    """
    Estimate the materials needed for toilets.

    Parameters:
    num_toilets (int): Number of toilets.
    weight_per_toilet (float): Weight of one toilet in kilograms.

    Returns:
    dict: A dictionary containing the estimated weight of each material in the toilets.
    """
    material_pct = {'porcelain': 0.85, 'plastic': 0.10, 'stainless steel': 0.05}
    material_weights = {material: weight_per_toilet * pct * num_toilets for material, pct in material_pct.items()}
    return material_weights

def estimate_shower_materials(num_showers, weight_per_shower):
    """
    Estimate the materials needed for showers.

    Parameters:
    num_showers (int): Number of showers.
    weight_per_shower (float): Weight of one shower in kilograms.

    Returns:
    dict: A dictionary containing the estimated weight of each material in the showers.
    """
    material_pct = {'glass': 0.50, 'plastic': 0.30, 'stainless steel': 0.20}
    material_weights = {material: weight_per_shower * pct * num_showers for material, pct in material_pct.items()}
    return material_weights

def estimate_sink_materials(num_sinks, weight_per_sink):
    """
    Estimate the materials needed for sinks.

    Parameters:
    num_sinks (int): Number of sinks.
    weight_per_sink (float): Weight of one sink in kilograms.

    Returns:
    dict: A dictionary containing the estimated weight of each material in the sinks.
    """
    material_pct = {'porcelain': 0.70, 'plastic': 0.20, 'stainless steel': 0.10}
    material_weights = {material: weight_per_sink * pct * num_sinks for material, pct in material_pct.items()}
    return material_weights

def estimate_bathtub_materials(num_bathtubs, weight_per_bathtub):
    """
    Estimate the materials needed for bathtubs.

    Parameters:
    num_bathtubs (int): Number of bathtubs.
    weight_per_bathtub (float): Weight of one bathtub in kilograms.

    Returns:
    dict: A dictionary containing the estimated weight of each material in the bathtubs.
    """
    material_pct = {'acrylic': 0.80, 'plastic': 0.10, 'cast iron': 0.10}
    material_weights = {material: weight_per_bathtub * pct * num_bathtubs for material, pct in material_pct.items()}
    return material_weights
