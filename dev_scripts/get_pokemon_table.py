"""Download and save a master pokemon table json."""

# import requests
# from pathlib import Path
# import json

# url = "https://github.com/itsjavi/supereffective.gg/blob/main/src/lib/data-client/pokemon/legacy-pokemon.json"

# response = requests.get(url)
# response.raise_for_status()

# data = response.json()
# output_path = Path("apriscout/dev_scripts/pokemon.json")

# with output_path.open("w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)

# print(f"JSON saved to {output_path.resolve()}")
