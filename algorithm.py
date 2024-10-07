import random
import copy

perk_list = {
    "weapons": {
        "small_calibre": {
            "name": "Small Calibre",
            "cost": 0,
        },
        "peacekeeping": {
            "name": "Peacekeeping",
            "cost": 2,
        },
        "close_quarters": {
            "name": "Close Quarters",
            "cost": 2,
        },
        "long_range": {
            "name": "Long Range",
            "cost": 3,
        },
    },
    "diving": {
        "basics": {
            "name": "Basics",
            "cost": 0,
        },
        "mobility_pack": {
            "name": "Mobility Pack",
            "cost": 2,
        },
        "boarding_kits": {
            "name": "Boarding Kits",
            "cost": 3,
        },
    },
    "engineering": {
        "ship_repair": {
            "name": "Ship Repair",
            "cost": 0,
        },
        "incendium_pack": {
            "name": "Incendium Pack",
            "cost": 2,
        },
        "exosuit": {
            "name": "Exosuit",
            "cost": 2,
        },
        "sabotage": {
            "name": "Sabotage",
            "cost": 2,
        },
        "raw_materials": {
            "name": "Raw Materials",
            "cost": 4,
        },
    },
    "upgrades": {
        "steel": {
            "name": "Steel",
            "cost": 0,
        },
        "titanium_aluminium_alloy": {
            "name": "Titanium Aluminium Alloy",
            "cost": 4,
            "dependant": "steel",
        },
        "physicorium": {
            "name": "Physicorium",
            "cost": 3,
            "dependant": "titanium_aluminium_alloy",
        },
    },
    "medical": {
        "first_aid": {
            "name": "First Aid",
            "cost": 0,
        },
        "lifesavers": {
            "name": "Lifesavers",
            "cost": 2,
        },
        "combat_drugs": {
            "name": "Combat Drugs",
            "cost": 2,
        },
    },
    "talents": {
        "basic": {
            "name": "Basic",
            "cost": 1,
        },
        "advanced": {
            "name": "Advanced",
            "cost": 2,
            "dependant": "basic",
        },
        "elite": {
            "name": "Elite",
            "cost": 4,
            "dependant": "advanced",
        },
    },
    "turrets": {
        "small_hardpoints": {
            "coilgun": {
                "name": "Coilgun",
                "cost": 1,
            },
            "chaingun": {
                "name": "Chaingun",
                "cost": 2,
            },
            "pulse_laser": {
                "name": "Pulse Laser",
                "cost": 2,
            },
        },
        "large_hardpoints": {
            "railgun": {
                "name": "Railgun",
                "cost": 3,
            },
            "flak_cannon": {
                "name": "Flak Cannon",
                "cost": 3,
            },
            "double_coilgun": {
                "name": "Double Coilgun",
                "cost": 3,
            }
        }
    }
}

def generate_points(p):
    # Adjust weight factor based on max 16 players
    weight_factor = p / 75  # 75 is arbitrary number, it's somewhat balanced for a max of 16 player to average roughly half the max points every round, lesser number means more points, higher number means less points
    
    # Generate weights to favor higher numbers as p increases
    weights = [(i / 45) ** weight_factor for i in range(0, 45 + 1)]
    
    # Normalize weights
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    # Randomly choose a value for p based on the weights
    p = random.choices(range(0, 45 + 1), weights=normalized_weights)[0]
    
    return p

def generate_perks(points):
    n = 0
    # Initialize empty list of perks
    perks = []
    # Create a copy of the perk list
    perk_list_copy = copy.deepcopy(perk_list)
    # Track if a turret from small or large hardpoints has been selected
    turret_selected = {"small_hardpoints": False, "large_hardpoints": False}
    
    # Check for the while loop
    check = True
    
    # Generate perks until we run out of points
    while check:
        # Get list of categories that still have available perks
        available_categories = [category for category in perk_list_copy if perk_list_copy[category]]

        # If there are no available categories left, break the loop
        if not available_categories:
            break
        
        # Choose a random category
        category = random.choice(available_categories)
        
        # Get list of available perks or subcategories in the chosen category
        available_perks_or_subcategories = list(perk_list_copy[category].keys())
        
        # If no perks or subcategories are left, skip this category
        if not available_perks_or_subcategories:
            continue
        
        # Choose a random perk or subcategory
        perk_or_subcategory = random.choice(available_perks_or_subcategories)

        n += 1
        if n > points:
            return perks
        
        # If the selected item is a subcategory (i.e., a dictionary), pick a perk from within it
        if isinstance(perk_list_copy[category][perk_or_subcategory], dict) and "cost" not in perk_list_copy[category][perk_or_subcategory]:
            # Handle subcategory like "small_hardpoints" or "large_hardpoints"
            subcategory = perk_or_subcategory
            
            # Skip picking another turret from this subcategory if a turret has already been selected
            if turret_selected[subcategory]:
                continue

            # Randomly choose a perk from the subcategory
            perk = random.choice(list(perk_list_copy[category][subcategory].keys()))
            perk_data = perk_list_copy[category][subcategory][perk]
            
            # After selecting a turret, mark the subcategory as already selected
            turret_selected[subcategory] = True
        else:
            # Otherwise, it's a direct perk
            perk_data = perk_list_copy[category][perk_or_subcategory]
        
        # Check for dependency in the "upgrades" category
        if category in ["upgrades", "talents"] and "dependant" in perk_data:
            dependant_perk = perk_data["dependant"]
            # If the required perk hasn't been selected yet, skip this perk
            if dependant_perk not in perks:
                continue
        
        # Check if the player can afford the perk
        if perk_data["cost"] <= points:
            # Add the perk to the list
            perks.append(perk_data["name"])
            
            # Deduct the cost of the perk from the player's points
            points -= perk_data["cost"]

            # Remove the perk directly (for direct perks)
            if not isinstance(perk_list_copy[category][perk_or_subcategory], dict) or "cost" in perk_list_copy[category][perk_or_subcategory]:
                del perk_list_copy[category][perk_or_subcategory]
        else:
            # Stop if we can't afford the perk
            check = False 
    
    return perks

def flatten_perk_list(perk_dict):
    flat_list = []
    
    for key, value in perk_dict.items():
        if isinstance(value, dict):
            # If it's a dictionary, check if it has a 'name'
            if 'name' in value:
                flat_list.append(value['name'])  # Add the perk name
            else:
                # Recursively flatten subcategories
                flat_list.extend(flatten_perk_list(value))
    
    return flat_list

def sort_perks(perks):
    # Flatten the perk list
    flat_perk_list = flatten_perk_list(perk_list)

    # Check if all perks are in the flat list
    for perk in perks:
        if perk not in flat_perk_list:
            print(f"Warning: '{perk}' not found in the flat perk list.")
    
    # Sort the perks based on their order in the flat list
    sorted_perks = sorted(perks, key=lambda x: flat_perk_list.index(x) if x in flat_perk_list else float('inf'))
    
    return sorted_perks

# Example of generating and sorting perks
points = generate_points(5)
print(f"Points: {points}")
print("------------------------")

# Generate and sort perks
perks = generate_perks(points)
sorted_perks = sort_perks(perks)
print("Sorted Perks:")
for perk in sorted_perks:
    print(perk)
print("------------------------")