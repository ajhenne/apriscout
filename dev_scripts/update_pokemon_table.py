"""Populate the Pokemon database table from the JSON file."""

import os
import json
from apriscout import create_app, db
from apriscout.models import Pokemon
import glob

SPRITE_FOLDER = "sprites/pokemon"
JSON_PATH = "dev_scripts/legacy-pokemon.json"

app = create_app()


def get_missing_sprites():
    """Find missing Pokemon sprites by cycling through images."""

    filepath = "/Users/ah724/Documents/apriscout/apriscout/static/sprites/pokemon/"

    no_sprite = []
    for i in range(1, 1533):
        if not os.path.isfile(filepath + str(i) + ".png"):
            no_sprite.append(i)

    return no_sprite


def get_problem_sprites():
    """Just a list of problematic Pokemon/sprites."""

    return [x for x in range(1528, 1551)] + [1600]


with app.app_context():

    # Clear the table if needed
    db.session.query(Pokemon).delete()

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    missing_sprites = get_missing_sprites()
    problem_sprites = get_problem_sprites()

    for id, entry in enumerate(data):

        id += 1

        if id in missing_sprites or id in problem_sprites:
            continue

        name = entry["name"]
        dex_num = entry["dexNum"]
        form_id = entry["formId"]
        is_female = entry["isFemaleForm"]
        generation = entry["generation"]
        type1 = entry["type1"]
        type2 = entry["type2"]
        sprite = f"{SPRITE_FOLDER}/{id}.png"

        if Pokemon.query.filter_by(name=name).first():
            continue

        pokemon = Pokemon(
            id=id,
            name=name,
            dex_num=dex_num,
            form_id=form_id,
            is_female=is_female,
            generation=generation,
            type1=type1,
            sprite=sprite,
        )

        db.session.add(pokemon)

    db.session.commit()
    print("Pokemon table populated.")
