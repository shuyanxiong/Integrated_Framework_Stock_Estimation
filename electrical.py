import math

# @ electrical_cable
# Total Wire Length = (Distance from Electrical Panel to Room + Distance between Outlets and Fixtures) x Number of Outlets and Fixtures x 1.25 (safety factor)
# distance from electrical panel to room = half perimeter of the rooms
# distance between outlets and fixtures = 1m
# https://www.thespruce.com/electrical-code-for-outlets-1821513
# number of outlets and fixtures = 1 outlet + 1 light + 1 switch + 1 GFCI outlet + 1 smoke detector + 1 CO detector = 5 per room

def calculate_electrical_cable_length_per_apartment(living_space, num_rooms):
    a = 5 # assuming 5 outlets
    b = 1.25 # safety factor
    cable_length_apartment= 2 * (living_space ** 0.5) * a * b * num_rooms # assuming duct length is half perimeter of each apartment
    return cable_length_apartment

def calculate_electrical_cable_length(floor_height, total_cable_length_horizontal, num_floors):
    # assuming electrical wire uniform for now
    buffer = 0.15 # Fitting Factor (typically 0.10 to 0.15 for 10-15% additional length)
    electrical_wire_length = (total_cable_length_horizontal + floor_height * num_floors * 2 )* (1 + buffer) if num_floors > 0 else total_cable_length_horizontal
    
    return electrical_wire_length

def calculate_electrical_cable_weight(electrical_wire_length, density): # 4065
    # Cross-sectional area of wire in circular mils
    # https://www.omnicalculator.com/physics/copper-wire-weight
    # 12 guage = 0.0808 inch = 2.032 mm
    # area = math.pi * (0.002/2) ** 2
    weight = electrical_wire_length * density
    return weight


# Example Calculation:
# Assume we have a 3-core copper cable with PVC insulation.

# Specifications:

# Conductor Cross-Section: 2.5 mm²
# Insulation Thickness: 0.8 mm
# Cable Diameter with Insulation: 5.5 mm (approx)
# Copper Density: 8.96 g/cm³
# PVC Density: 1.4 g/cm³
# Steps:

# Calculate Volume of Copper:

# Volume per meter of copper (V_copper) = Cross-sectional area x Length
# V_copper = 2.5 mm² x 3 (cores) = 7.5 mm²
# Convert to cm³: 7.5 mm² = 0.75 cm² (since 1 cm² = 100 mm²)
# Calculate Weight of Copper:

# Weight of copper per meter = Volume x Density
# Weight_copper = 0.75 cm² x 100 cm (length) x 8.96 g/cm³
# Weight_copper = 0.75 x 8.96 g = 6.72 g per meter
# Calculate Volume of Insulation:

# Assuming insulation is a cylindrical layer around the conductor.
# Outer diameter = 5.5 mm, inner diameter = conductor diameter
# Insulation volume = π/4 x (outer² - inner²) x length
# Inner diameter (approx): 2.5 mm (assume no gap)
# Volume of insulation per meter: π/4 x ((5.5 mm)² - (2.5 mm)²) x 100 cm
# V_insulation ≈ 3.14/4 x (30.25 - 6.25) x 100 cm = 3.14/4 x 24 x 100 cm = 188.4 cm³/m
# Calculate Weight of Insulation:

# Weight of PVC per meter = Volume x Density
# Weight_PVC = 188.4 cm³ x 1.4 g/cm³ = 263.76 g per meter
# Total Cable Density:

# Total weight = Weight_copper + Weight_PVC
# Total weight ≈ 6.72 g + 263.76 g = 270.48 g per meter
# 4. Constitution Percentage
# To find the constitution percentage of each material in the cable:

# Copper Percentage:

# Copper weight percentage = (Weight_copper / Total weight) x 100
# Copper percentage = (6.72 / 270.48) x 100 ≈ 2.49%
# PVC Percentage:

# PVC weight percentage = (Weight_PVC / Total weight) x 100
# PVC percentage = (263.76 / 270.48) x 100 ≈ 97.51%


def estimate_electrical_cable_materials(weight):
    # http://www.thelen.us/1wire.php
    # Please find the cable data from one of the reputed manufacturing companies from Saudi Arabia for low voltage copper cables as per IEC-502 standard.

    # PVC/PVC insulated Unarmed Cables of size 300mm2
    # Weight of the three core cable with insulation = 10805Kg/km
    # Weight of the sing core cable with insulation = 3420Kg/km

    # PVC/PVC insulated Steel Wire Armed Cables of size 300mm2
    # Weight of the three core cable with insulation = 13500Kg/km
    # Weight of the sing core cable with insulation = 4065Kg/km

    # Copper Wire without insulation of size 300mm2
    # Weight of the single bare copper wire of 300mm2 (without insulation) = 2627kg/km
    # 2.5mm2 22.4g/m and 50g/m with insulation
    material_pct = {
        'copper': 0.45,
        'pvc': 0.55
    }
    
    # Calculate estimated material weights based on percentages
    material_weights = {material: weight * pct for material, pct in material_pct.items()}
    
    return material_weights

# def calculate_electrical_cable_length_per_building(floor_height, living_space_per_apartment,num_floors, electrical_wire_length, density=4065):
#     a = 3 # assuming 5 outlets
#     b = 1.25 # safety factor

#     total_duct_length_horizontal= sum([2 * (area ** 0.5) * a * b  for area in living_space_per_apartment])
#     # assuming electrical wire uniform for now
#     electrical_wire_length = (total_duct_length_horizontal + floor_height) * num_floors
    
#     weight = electrical_wire_length/1000 * density
    
#     return weight