import itertools
import random

# Define unit stats and costs
unit_stats = {
    'Fighter': {'combat': 9, 'cost': 0.5, 'capacity': 0, 'sustain_damage': True},
    'Carrier': {'combat': 9, 'cost': 3, 'capacity': 6, 'sustain_damage': False},
    'Destroyer': {'combat': 9, 'cost': 1, 'capacity': 0, 'sustain_damage': False},
    'Cruiser': {'combat': 7, 'cost': 2, 'capacity': 0, 'sustain_damage': False},
    'Dreadnought': {'combat': 5, 'cost': 4, 'capacity': 1, 'sustain_damage': True},
    'WarSun': {'combat': 6, 'cost': 12, 'capacity': 3, 'sustain_damage': True},
}

# Define fleet capacity range
fleet_capacity_range = range(1, 11)

# Define the number of simulations
num_simulations = 1000

def simulate_battle(attacker, defender):
    # # Convert Fighter cost to .5
    # for unit in attacker + defender:
    #     if unit == 'Fighter':
    #         unit_stats[unit]['cost'] = 0.5

    # Function to determine the cost of a unit
    def unit_cost(unit_type):
        return unit_stats[unit_type]['cost']

    # Function to simulate a round of combat
    def combat_round(attacking_units, defending_units):
        attack_hits = sum(random.randint(1, 10) <= unit_stats[unit]['combat'] for unit in attacking_units)
        defense_hits = sum(random.randint(1, 10) <= unit_stats[unit]['combat'] for unit in defending_units)
        return attack_hits, defense_hits

    # Sort units by cost (cheapest to most expensive)
    attacker.sort(key=unit_cost)
    defender.sort(key=unit_cost)

    # Initialize sustain damage for each ship
    for unit_type in attacker + defender:
        unit_stats[unit_type]['remaining_sustain_damage'] = unit_stats[unit_type]['sustain_damage']

    # Main battle loop
    while attacker and defender:
        attack_hits, defense_hits = combat_round(attacker, defender)

        # Apply hits to defending units with sustain damage
        for unit_type in defender:
            if unit_stats[unit_type]['remaining_sustain_damage'] > 0:
                unit_stats[unit_type]['remaining_sustain_damage'] -= min(defense_hits, unit_stats[unit_type]['remaining_sustain_damage'])
                defense_hits -= unit_stats[unit_type]['remaining_sustain_damage']

        # Remove destroyed ships
        defender = defender[:-defense_hits] if defense_hits > 0 else defender
        attacker = attacker[:-attack_hits] if attack_hits > 0 else attacker

    # Determine the winner
    winner = 'Attacker' if attacker else 'Defender' if defender else 'Draw'
    
    return attacker, defender, winner

# Example usage:
attacker_units = ['Fighter', 'Fighter', 'Cruiser', 'Destroyer']
defender_units = ['Dreadnought', 'Carrier', 'Fighter', 'Fighter']

print(f"Battle between Attacker: {attacker_units} and Defender: {defender_units}")
result = simulate_battle(attacker_units, defender_units)
print(f"Attacker: {result[0]}, Defender: {result[1]}, Winner: {result[2]}")

# # Function to simulate battles
# def simulate_battles(army1, army2):
#     wins = 0
#     for _ in range(num_simulations):
#         result = random.choice([1, 2])  # Simulate a simple win/loss scenario
#         if result == 1:
#             wins += 1
#     return wins

# # Generate all possible combinations of units
# unit_combinations = []
# for capacity in fleet_capacity_range:
#     for combination in itertools.product(unit_stats.keys(), repeat=capacity):
#         if all(unit_stats[unit]['capacity'] <= capacity for unit in combination):
#             unit_combinations.append(combination)

# # Perform simulations
# for army1 in unit_combinations:
#     total_wins = 0
#     army1_cost = sum(unit_stats[unit]['cost'] for unit in army1)
    
#     print(f"Army Composition ({army1_cost} Resources): {', '.join(army1)}")

#     for army2 in unit_combinations:
#         army2_cost = sum(unit_stats[unit]['cost'] for unit in army2)
#         wins = simulate_battles(army1, army2)
#         total_wins += wins

#         print(f"  Against Enemy Composition ({army2_cost} Resources): {', '.join(army2)} - {wins} wins")

#     win_percentage = (total_wins / (num_simulations * len(unit_combinations))) * 100
#     print(f"  Total Win Percentage: {win_percentage:.2f}%\n")
