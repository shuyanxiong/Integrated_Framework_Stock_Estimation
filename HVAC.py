import math
import numpy as np

# @ Raditor
# calculate the number of radiators needed for each apartment
def calculate_radiators_per_apartment(heated_area, num_rooms,num_kitchens): 
    a = 1 # assume 1 radiator per room
    # # calculate the heat loss rate based on the insulation level
    # if insulation == "poor":
    #     heat_loss_rate = 100
    # elif insulation == "average":
    #     heat_loss_rate = 80
    # else:
    #     heat_loss_rate = 60
    heat_loss_rate = 80
    # calculate the total heat loss for the property
    total_heat_loss = heated_area * heat_loss_rate
    radiator_capacity = 1500
    # calculate the number of radiators needed based on the heating system's capacity
    num_radiators = np.ceil(total_heat_loss / radiator_capacity)  # assuming a heating system capacity of 1.5 kW per radiator

    # calculate the total number of radiators needed
    # assume 1 radiator per bedroom, bathroom, living room and kitchen
    total_num_radiators = a * num_rooms + num_kitchens
    return int(np.max([total_num_radiators, num_radiators])) # round up the number of radiators to the nearest integer

# def estimate_materials_radiator(weight_kg):
#     material_pct = {
#         'steel': 0.85,
#         'copper': 0.1,
#         'plastic': 0.05
#     }
    
#     # Calculate estimated material weights based on percentages
#     material_weights = {material: weight_kg * pct for material, pct in material_pct.items()}
    
    # return material_weights

# Radiator data by decade
radiator_data = {
    '1930s and below': {'type': 'no radiator', 'material': 'cast iron', 'unit_weight': 0, 'lifespan': 20},
    '1940s': {'type': 'cast iron radiator', 'material': 'cast iron', 'unit_weight': 63, 'lifespan': 20},
    '1950s': {'type': 'steel panel radiator', 'material': 'steel', 'unit_weight': 21, 'lifespan': 50},
    '1960s': {'type': 'convector radiator', 'material': 'steel', 'unit_weight': 42, 'lifespan': 30},
    '1970s': {'type': 'column radiator', 'material': 'cast iron', 'unit_weight': 82, 'lifespan': 50},
    '1980s': {'type': 'steel panel radiator', 'material': 'steel', 'unit_weight': 21, 'lifespan': 50},
    '1990s': {'type': 'low surface temperature (LST) radiator', 'material': 'steel', 'unit_weight': 38, 'lifespan': 50},
    '2000s and beyond': {'type': 'low surface temperature (LST) radiator', 'material': 'steel', 'unit_weight': 38, 'lifespan': 50}
}

# Material composition for each radiator type
radiator_material_composition = {
    'cast iron radiator': {'cast iron': 0.95, 'plastic': 0.05},
    'steel panel radiator': {'steel': 0.85, 'plastic': 0.05, 'copper': 0.1},
    'convector radiator': {'steel': 0.8, 'copper': 0.15, 'plastic': 0.05},
    'column radiator': {'cast iron': 0.90, 'plastic': 0.05, 'copper': 0.05},
    'low surface temperature (LST) radiator': {'steel': 0.75, 'copper': 0.15, 'plastic': 0.1}
}


# # Function to calculate the decade based on building year
# def get_decade(building_year):
#     # Use formula to calculate the starting year of the decade
#     decade_start = (building_year // 10) * 10
#     return f"{decade_start}s"

# Function to determine the decade based on the specific building year
def get_decade(building_year):
    if building_year < 1940:
        return '1930s and below'
    if 1940 <= building_year < 1950:
        return '1940s'
    elif 1950 <= building_year < 1960:
        return '1950s'
    elif 1960 <= building_year < 1970:
        return '1960s'
    elif 1970 <= building_year < 1980:
        return '1970s'
    elif 1980 <= building_year < 1990:
        return '1980s'
    elif 1990 <= building_year < 2000:
        return '1990s'
    else:  # for 2000 and beyond
        return '2000s and beyond' # For buildings built in or after 2010
    
# Function to estimate material distribution based on radiator type
def estimate_materials_radiator(weight_kg, radiator_type):
    if radiator_type not in radiator_material_composition:
        raise ValueError(f"Radiator type {radiator_type} is not in the material composition database.")
    
    # Get the material composition for the given radiator type
    material_pct = radiator_material_composition[radiator_type]
    
    # Calculate estimated material weights based on percentages
    material_weights = {material: weight_kg * pct for material, pct in material_pct.items()}
    
    return material_weights

# # Function to determine the radiator type and estimate materials based on building age
# def estimate_radiator_by_building_age(building_year, weight_kg):
#     # Get the decade based on building year using the new formula
#     decade = get_decade(building_year)
    
#     # Check if the decade is in the radiator data
#     if decade not in radiator_data:
#         raise ValueError(f"Radiator data for the decade {decade} is not available.")
    
#     # Get radiator type based on the decade
#     radiator_type = radiator_data[decade]['type']
    
#     # Estimate material distribution for the determined radiator type
#     material_weights = estimate_materials_radiator(weight_kg, radiator_type)
    
#     return radiator_type, material_weights

# Function to determine the radiator type and estimate materials based on building age
def estimate_radiator_by_building_age(building_year, weight_kg):
    # Get the decade based on building year using the new formula
    decade = get_decade(building_year)
    
    # Check if the decade is in the radiator data
    if decade not in radiator_data:
        raise ValueError(f"Radiator data for the decade {decade} is not available.")
    
    # Get radiator type based on the decade
    radiator_type = radiator_data[decade]['type']
    
    # Check if the radiator type is "no radiator" and return zero weights if true
    if radiator_type == "no radiator":
        return radiator_type, {'total_weight': 0}  # or return an empty dict or None as desired
    
    # Estimate material distribution for the determined radiator type
    material_weights = estimate_materials_radiator(weight_kg, radiator_type)
    
    return radiator_type, material_weights


# @ Boiler
def calculate_boiler_weight(total_num_radiators):
    # coefficient for heat output estimation
    c = 1.5
    d = 3
    heat_output= c * total_num_radiators + d
    # coefficients for boiler weight estimation
    a = 1.1 # 0.9, 1.1, 1.2
    b = 35 # 20, 35, 40
    weight = a * heat_output + b
    return weight

# material constitution of the boiler
def estimate_boiler_materials(weight_kg):
    # Material composition breakdown of a modern gas-fired condensing boiler: (approximate percentages)
    material_pct = {
        'steel': 0.75,
        'copper': 0.1,
        'plastic': 0.05,
        'mineral wool': 0.05,
        'aluminum': 0.02,
        'brass': 0.02,
        #  refractory materials, electronics, etc.
        'other electronics': 0.01
    }

    # Calculate estimated material weights based on percentages
    material_weights = {material: weight_kg * pct for material, pct in material_pct.items()}
    
    return material_weights

# @ Heat Pump
# Estimate the size of a heat pump needed for a building
# https://www.imsheatpumps.co.uk/blog/what-size-heat-pump-do-i-need-for-my-house/
# https://entreprisesmst.com/en/blog/heat-pump/how-do-i-determine-the-size-of-heat-pump-i-need-for-my-home/#:~:text=General%20rules%20for%20a%20rough%20calculation&text=For%20a%20heat%20pump%20or,be%20reduced%20to%209%2C000%20BTU.
# https://carbonswitch.com/heat-pump-sizing-guide/#:~:text=If%20you%20Google%20%E2%80%9Cheat%20pump,a%2060%2C000%20BTU%20heat%20pump.

def heat_pump_weight(building_size):
    # Rough estimate for heat pump weight in kg from https://sprsunheatpump.com/17-5KW-27KW-High-Cop-Air-to-Water-Heat-Pump-for-Floor-Heating-Water-Heater-pd6267665.html
    a = 30 
    b = 3412
    # weight coefficient
    c = 65
    d = 5
    efficiency_factor = 1 # 0.8 - 1.4
    size_factor = 0.9 # 0.9 - 1.1

    heat_pump_size = building_size * a / b * size_factor * efficiency_factor 
    weight = c + d * heat_pump_size
    return weight

# material constitution of the heat pump
def estimate_heat_pump_materials(weight_kg):
    # Material composition breakdown of a modern heat pump: (approximate percentages)
    # Heat Pump Model: ABC Air-Source Heat Pump
    # Material Contribution:
    # Compressor: 35% (typically made of steel, aluminum, and copper)
    # Heat Exchanger Coils: 25% (typically made of copper and aluminum)
    # Refrigerant: 20% (various refrigerants can be used, but most commonly hydrofluorocarbons, or HFCs)
    # Cabinet/Enclosure: 15% (typically made of sheet metal, such as galvanized steel or aluminum)
    # Control and Safety Devices: 5% (made up of various materials such as plastics, metals, and electronic components)

    material_pct = {
        'steel': 0.35,
        'aluminum': 0.20,
        'copper': 0.30,
        'plastic': 0.10,
        'refrigerant': 0.05
    }
    
    # Calculate estimated material weights based on percentages
    material_weights = {material: weight_kg * pct for material, pct in material_pct.items()}
    
    return material_weights

# @ air ducts

# assuming duct length in each room is half perimeter of the room

def select_duct_material(building_year):
    """
    Select the air duct material based on the building's construction year.

    Parameters:
    building_year (int): The year the building was constructed.

    Returns:
    str: The material of the air ducts.
    float: The density of the air duct material in kg/m³.
    dict: The percentage composition of materials.
    """
    if building_year < 1950:
        return "Galvanized Steel", 14, {'steel': 0.70, 'mineral wool': 0.3} #kg/m # https://library.walraven.com/repository/rnd/documents/Air-Duct-Dimensions-and-Weights-data-sheet-EN.pdf
    elif building_year < 1980:
        return "Aluminum", 2.34, {'aluminum': 0.23,'polyurethane foam':0.77} # https://www.siglers.com/4-aluminum-flex-duct-101000226978.html
    elif building_year < 2000:
        return "Fiberglass", 0.387, {'fiberglass': 0.5, 'aluminum': 0.5}  # https://lueftungsteile.ch/schlaeuche/184-1406-sonoflex-schlauch-akustisch-isoliert-10m.html#/58-durchmesser-300_mm
        # # Given data
        # inner_diameter = 0.3  # meters (300 mm)
        # outer_diameter = 0.325  # meters (325 mm)
        # aluminum_thickness = 0.000075  # meters (3 layers of 25 µm aluminum)
        # aluminum_density = 2700  # kg/m³
        # glass_fiber_density = 16  # kg/m³
        # glass_fiber_thickness = 0.025  # meters (25 mm insulation thickness)
        # length = 1  # meter for calculation

        # # Surface area of the inner duct (cylinder) for aluminum
        # inner_surface_area = math.pi * inner_diameter * length  # m²

        # # Weight of aluminum (inner duct)
        # aluminum_weight = aluminum_thickness * aluminum_density * inner_surface_area

        # # Volume of glass fiber insulation (as a cylindrical shell)
        # insulation_volume = math.pi * ((outer_diameter / 2) ** 2 - (inner_diameter / 2) ** 2) * length  # m³

        # # Weight of glass fiber insulation
        # glass_fiber_weight = insulation_volume * glass_fiber_density

        # # Total weight
        # total_weight = aluminum_weight + glass_fiber_weight

        # # Material percentages
        # aluminum_percentage = (aluminum_weight / total_weight) * 100
        # glass_fiber_percentage = (glass_fiber_weight / total_weight) * 100

        # total_weight, aluminum_percentage, glass_fiber_percentage

    else:
        return "Flexible Duct (Plastic)", 1.9, {'plastic': 0.80, 'steel': 0.20}  # https://www.absaugtechnik.ch/pe-absaugschlauch-225-mm-leicht-und-flexibel-pe95225?gad_source=1&gclid=CjwKCAjwjsi4BhB5EiwAFAL0YC8Xr-3ufTP3A3b8NmtCXcPP2V2Lcu7jqqWmLN622DaxnOYmUqUpnhoCPFwQAvD_BwE

def calculate_HVAC_pipe_length_per_apartment(living_space, num_rooms):
    """
    Calculate the total HVAC duct length needed for an apartment.

    Parameters:
    living_space (float): The area of the living space in square meters.
    num_rooms: supply points

    Returns:
    float: The estimated duct length for the apartment.
    """
    duct_length_apartment = (living_space ** 0.5)/2 * num_rooms # Assuming duct length from main supply point to each air outlet is 1/8 perimeter of each apartment
    return duct_length_apartment

def calculate_HVAC_pipe_length(floor_height, total_duct_length_horizontal_apartment, building_area, num_floors):
    """
    Calculate the total length of HVAC ducts needed for the building.

    Parameters:
    floor_height (float): The height of each floor in meters.
    total_duct_length_horizontal (float): The total horizontal duct length per floor in meters.
    num_floors (int): The number of floors in the building.

    Returns:
    float: The total length of HVAC ducts needed.
    """
    buffer = 0.15 # Fitting Factor (typically 0.10 to 0.15 for 10-15% additional length)
    total_duct_length = (total_duct_length_horizontal_apartment + (building_area**0.5)*2 + 2 * floor_height * num_floors) * (1 + buffer) if num_floors > 0 else total_duct_length_horizontal_apartment
    return total_duct_length

# def calculate_HVAC_pipe_weight(duct_length, width, height, outer_diameter, wall_thickness, density, is_rectangular=True):
#     """
#     Calculate the total weight of the HVAC ducts.

#     Parameters:
#     duct_length (float): The total length of the HVAC ducts in meters.
#     width (float): The width of the rectangular duct in meters.
#     height (float): The height of the rectangular duct in meters.
#     outer_diameter (float): The outer diameter of the circular duct in meters.
#     wall_thickness (float): The thickness of the duct walls in meters.
#     density (float): The density of the duct material in kg/m³.
#     is_rectangular (bool): True if the duct is rectangular, False if circular.

#     Returns:
#     float: The total weight of the HVAC ducts in kilograms.
#     """
#     if is_rectangular:
#         # Calculate cross-sectional area and volume
#         cross_sectional_area = height * width - (height - 2 * wall_thickness) * (width - 2 * wall_thickness)
#         volume = cross_sectional_area * duct_length
        
#         # Calculate weight using density
#         weight = volume * density
#     else:
#         # Calculate inner diameter
#         inner_diameter = outer_diameter - 2 * wall_thickness
        
#         # Calculate cross-sectional area and volume
#         cross_sectional_area = math.pi / 4 * (outer_diameter ** 2 - inner_diameter ** 2)
#         volume = cross_sectional_area * duct_length
        
#         # Calculate weight using density
#         weight = volume * density
        
#     return weight

def calculate_HVAC_pipe_weight(duct_length, density):
    weight = duct_length * density
    return weight 


def estimate_HVAC_pipe_materials(weight_kg, material_pct):
    """
    Estimate the material composition breakdown of the HVAC ducts.

    Parameters:
    weight_kg (float): The total weight of the HVAC ducts in kilograms.
    material_pct (dict): The percentage composition of materials.

    Returns:
    dict: A dictionary containing the estimated weight of each material in the ducts.
    """
    material_weights = {material: weight_kg * pct for material, pct in material_pct.items()}
    return material_weights



