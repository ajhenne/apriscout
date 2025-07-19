"""Populate the Pokemon database table from the JSON file."""

import os
import json
import glob
import pandas as pd

from apriscout import create_app, db
from apriscout.models import Pokemon
from apriscout.constants import starter_names

SPRITE_FOLDER = "sprites/pokemon"
JSON_PATH = "dev_scripts/legacy-pokemon.json"

app = create_app()


with app.app_context():

    # Clear the table if needed
    db.session.query(Pokemon).delete()

    data = pd.read_csv("dev_scripts/pokemon_species.csv")

    for idx, row in data.iterrows():

        id = idx + 1
        name = row["identifier"]
        generation = row["generation_id"]
        evolves_from = row["evolves_from_species_id"]
        evolution_chain_id = row["evolution_chain_id"]
        female_difference = row["has_gender_differences"]
        is_starter = name.lower() in starter_names
        sprite = f"sprites/pokemon/{id}.png"

        if Pokemon.query.filter_by(name=name).first():
            continue

        pokemon = Pokemon(
            id=id,
            name=name,
            generation=generation,
            evolves_from=evolves_from,
            evolution_chain_id=evolution_chain_id,
            female_difference=female_difference,
            is_starter=is_starter,
            sprite=sprite,
        )

        db.session.add(pokemon)

    db.session.commit()
    print("Pokemon table populated.")
