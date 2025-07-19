"""Download and save a master pokemon table json."""

import requests
from pathlib import Path

url = "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv"

response = requests.get(url)
response.raise_for_status()  # Ensure we raise an error for bad responses

output_path = Path("dev_scripts/pokemon_species.csv")
output_path.write_bytes(response.content)
print(f"CSV downloaded and saved to {output_path}")


# id,identifier,generation_id,evolves_from_species_id,evolution_chain_id,color_id,shape_id,habitat_id,gender_rate,capture_rate,base_happiness,is_baby,hatch_counter,has_gender_differences,growth_rate_id,forms_switchable,is_legendary,is_mythical,order,conquest_order
# 1,bulbasaur,1,,1,5,8,3,1,45,70,0,20,0,4,0,0,0,1,
