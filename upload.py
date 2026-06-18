from spellParser import parse_spell_json
import pyodbc
from dotenv import load_dotenv
import os

def get_connection():
    load_dotenv()
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"Trusted_Connection=yes;"
    )
    return conn

def _get_dim_table_data(spells: dict):
    dim_data = {
        "schools": [],
        "classes": []
    }

    for spell in spells:
        school = spell["school"]
        classes_data = spell["classes"]

        if school not in dim_data["schools"]:
            dim_data["schools"].append(school)

        for class_data in classes_data:
            if class_data not in dim_data["classes"]:
                dim_data["classes"].append(class_data)

    return dim_data

def _insert_if_not_exists(cursor, table, value):
    sql = f"""
    IF NOT EXISTS (SELECT 1 FROM {table} WHERE name = ?)
    BEGIN
        INSERT INTO {table} (name) VALUES (?)
    END
    """
    cursor.execute(sql, value, value)

def insert_into_dim_tables(spells: dict):
    dim_data = _get_dim_table_data(spells)
    dim_tables = [
        {"table": "dim_schools", "values": dim_data["schools"]},
        {"table": "dim_classes", "values": dim_data["classes"]}
    ]

    conn = get_connection()

    cursor = conn.cursor()
    for table_data in dim_tables:
        table = table_data["table"]
        values = table_data["values"]

        for value in values:
            try:
                _insert_if_not_exists(cursor, table, value)
                conn.commit()
            except pyodbc.Error as e:
                print(f"Insert into {table} failed for {value}: \n{e}\n")
                conn.rollback()
    conn.close()

def _insert_into_fact_spells(spell: dict):
    conn = get_connection()
    cursor = conn.cursor()

    params = {
        "name": spell.get("name"),
        "level": spell.get("level"),
        "school_name": spell.get("school"),
        "action_type": spell.get("actionType"),
        "is_concentration": spell.get("concentration"),
        "is_ritual": spell.get("ritual"),
        "casting_time": spell.get("castingTime"),
        "range": spell.get("range"),
        "require_visual_component": "v" in spell.get("components"),
        "require_somatic_component": "s" in spell.get("components"),
        "require_material_component": "m" in spell.get("components"),
        "duration": spell.get("duration"),
        "description": spell.get("description"),
        "materials": spell.get("material"),
        "cantrip_upgrade": spell.get("cantripUpgrade"),
        "higher_level_slot": spell.get("higherLevelSlot"),
        "material_cost": spell.get("materialCost"),
        "does_spell_consume": spell.get("doesSpellConsume"),
        "saving_throw_type": spell.get("savingThrowType"),
        "is_half_damage_on_success": spell.get("isHalfDamageOnSuccess"),
        "does_damage": spell.get("doesDamage"),
        "is_exclusive": spell.get("isExclusive")
    }

    ordered_keys = [
        "name", "level", "school_name", "action_type", "is_concentration",
        "is_ritual", "casting_time", "range", "require_visual_component",
        "require_somatic_component", "require_material_component", "duration",
        "description", "materials", "cantrip_upgrade", "higher_level_slot",
        "material_cost", "does_spell_consume", "saving_throw_type",
        "is_half_damage_on_success", "does_damage", "is_exclusive"
    ]

    params_ordered = [params[k] for k in ordered_keys]
    placeholders = ", ".join(["?"] * len(params))
    cursor.execute(f"{{CALL usp_insert_spell({placeholders})}}", params_ordered)

    conn.commit()
    conn.close()

def _insert_into_bridge_spells_and_classes(spell: dict):
    conn = get_connection()
    cursor = conn.cursor()

    class_names = spell.get("classes")

    for class_name in class_names:
        params = {
            "spell_name": spell.get("name"),
            "class_name": class_name
        }

        ordered_keys = ["spell_name", "class_name"]

        params_ordered = [params[k] for k in ordered_keys]
        placeholders = ", ".join(["?"] * len(params))
        cursor.execute(f"{{CALL usp_insert_bridge_spell_and_class({placeholders})}}", params_ordered)

    conn.commit()
    conn.close()

def insert_into_spells(spells: dict):
    for spell in spells:
        _insert_into_fact_spells(spell)
        _insert_into_bridge_spells_and_classes(spell)

def main():
    spells = parse_spell_json()
    insert_into_dim_tables(spells)  
    insert_into_spells(spells)

if __name__ == '__main__':
    main()