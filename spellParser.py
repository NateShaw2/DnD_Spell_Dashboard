import os
import json
from dotenv import load_dotenv

def parse_spell_json():
    load_dotenv()
    file_path = os.getenv("FILE_PATH")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def main():
    print(json.dumps(parse_spell_json(), indent=2))

if __name__ == "__main__":
    main()