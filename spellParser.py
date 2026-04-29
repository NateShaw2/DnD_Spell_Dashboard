import os
import re
import json
from dotenv import load_dotenv
from enum import Enum

# Imports json of spells from a file specified in .env
# and returns the python dictionary version of that json.
def _import_spell_json():
    load_dotenv()
    file_path = os.getenv("FILE_PATH")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def _get_material_cost(spell):
    if "material" not in spell: 
        spell["material_cost"] = 0
        return

    words = re.sub(r"[^\w\s]", "", spell["material"]).lower().split()
    material_cost = 0
    for i, word in enumerate(words):
        if word == "gp" and i != 0:
            material_cost += int(words[i - 1])

    spell["material_cost"] = material_cost
    return

# Determines if a spell contains a material that is consumed on spell use.
# Logic is that it checks if the word consume appears in material field or description.
def _does_spell_consume(spell):
    try:
        # Check to see if word consume appears.
        if (re.search("consume", spell["material"].lower()) is not None
            or re.search("consume", spell["description"].lower()) is not None):
            spell["does_spell_consume"] = True
        else:
            spell["does_spell_consume"] = False

    except KeyError:
        spell["does_spell_consume"] = False

class _stat_type(Enum):
    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHAR = "charisma"

def _saving_throw_type(spell):
    word_list = spell["description"].lower().split()
    for i, word in enumerate(word_list):
        # Condition determines if a stat_type word is in the description followed
        # by the word "saving"
        if (word in _stat_type 
            and i < len(word_list) - 1 and word_list[i + 1] == "saving"):
            spell["saving_throw_type"] = word_list[i]
            return

    spell["saving_throw_type"] = None
    return

def _is_half_damage_on_success(spell):
    spell["is_half_damage_on_success"] = re.search(
        "half as much damage", spell["description"].lower()) is not None
    return


def parse_spell_json():
    data = _import_spell_json()
    for spell in data:
        _get_material_cost(spell)
        _does_spell_consume(spell)
        _saving_throw_type(spell)
        _is_half_damage_on_success(spell)

    return data

def main():
    print(json.dumps(parse_spell_json(), indent=2))

if __name__ == "__main__":
    main()