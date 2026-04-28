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

# Determines if a spell contains a material that is consumed on spell use.
# Logic is that it checks if the word consume appears in material field or description.
def _does_spell_consume(spell):
    try:
        if (re.search("consume", spell["material"]) is not None
            or re.search("consume", spell["description"]) is not None):
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
        if (word in _stat_type 
            and i < len(word_list) - 1 and word_list[i + 1] == "saving"):
            spell["saving_throw_type"] = word_list[i]
            return

    spell["saving_throw_type"] = None
    return

def parse_spell_json():
    data = _import_spell_json()
    for spell in data:
        _does_spell_consume(spell)
        _saving_throw_type(spell)

    return data

def main():
    print(json.dumps(parse_spell_json(), indent=2))

if __name__ == "__main__":
    main()