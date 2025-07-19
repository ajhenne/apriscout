"""Download and save a master pokemon table json."""

import requests
from pathlib import Path

url = "https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon_species.csv"

response = requests.get(url)
response.raise_for_status()  # Ensure we raise an error for bad responses

output_path = Path("dev_scripts/pokemon_species.csv")
output_path.write_bytes(response.content)
print(f"CSV downloaded and saved to {output_path}")
