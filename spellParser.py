import os
import re
import json
import argparse
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

def _get_material_cost(spell: dict):
    if "material" not in spell: 
        spell["materialCost"] = 0
        return

    words = re.sub(r"[^\w\s]", "", spell["material"]).lower().split()
    material_cost = 0
    for i, word in enumerate(words):
        if word == "gp" and i != 0:
            material_cost += int(words[i - 1])

    spell["materialCost"] = material_cost

# Determines if a spell contains a material that is consumed on spell use.
# Logic is that it checks if the word consume appears in material field or description.
def _does_spell_consume(spell: dict):
    try:
        # Check to see if word consume appears.
        if (re.search("consume", spell["material"].lower()) is not None
            or re.search("consume", spell["description"].lower()) is not None):
            spell["doesSpellConsume"] = True
        else:
            spell["doesSpellConsume"] = False

    except KeyError:
        spell["doesSpellConsume"] = False

class _stat_type(Enum):
    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHAR = "charisma"

def _saving_throw_type(spell: dict):
    word_list = spell["description"].lower().split()
    for i, word in enumerate(word_list):
        # Condition determines if a stat_type word is in the description followed
        # by the word "saving"
        if (word in _stat_type._value2member_map_ 
            and i < len(word_list) - 1 and word_list[i + 1] == "saving"):
            spell["savingThrowType"] = word_list[i]
            return

    spell["savingThrowType"] = None

def _is_half_damage_on_success(spell: dict):
    spell["isHalfDamageOnSuccess"] = re.search(
        "half as much damage", spell["description"].lower()) is not None

def _does_damage(spell: dict):
    # Regex determines if the word damage appears and if the actual dice damage
    # appears before the word damage appears.
    spell["doesDamage"] = re.search(
        r"\d+d\d.*damage", spell["description"]) is not None

# Determines if a spell only belongs to a single class.
def _is_exclusive(spell : dict):
    spell["isExclusive"] = len(spell["classes"]) == 1

class _damage_types(Enum):
    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"

def _damage_type(spell: dict):
    spell["damageTypes"] = []

    if spell["doesDamage"]:
        word_list = re.sub(r"[^\w\s]", "", spell["description"]).lower().split()

        for damage_type in _damage_types._value2member_map_:
            if damage_type in word_list:
                spell["damageTypes"].append(damage_type)

def parse_spell_json(damage_Type_On: bool = False):
    data = _import_spell_json()
    for spell in data:
        _get_material_cost(spell)
        _does_spell_consume(spell)
        _saving_throw_type(spell)
        _is_half_damage_on_success(spell)
        _does_damage(spell)

        if (damage_Type_On):
            _damage_type(spell)
        else: 
            spell["damageType"] = None

        _is_exclusive(spell)

    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--damageTypeOn", help="Adds damage type data", action="store_true")
    args = parser.parse_args()
    print(json.dumps(parse_spell_json(damage_Type_On = args.damageTypeOn), indent=2))

if __name__ == "__main__":
    main()