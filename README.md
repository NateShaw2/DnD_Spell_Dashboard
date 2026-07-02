# DnD_Spell_Dashboard

This ETL process and dashboard is based on DnD 2024 5e edition. The thought of this repo came about with my struggles finding spells for my new character — constantly flipping through the book or juggling a dozen browser tabs. This project lets you filter, search, and explore spells in one place through a Power BI dashboard.

## Overview

1. Spell data is loaded from a local JSON file and parsed by `spellParser.py`
2. `upload.py` transforms and inserts the parsed data into a local SQL Server database
3. A Power BI dashboard visualizes the spell data with filtering by class, school, level, and more

## Prerequisites

- Python 3.10+
- SQL Server (local instance with Windows Authentication)
- ODBC Driver 17 for SQL Server
- Power BI Desktop

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/DnD_Spell_Dashboard.git
cd DnD_Spell_Dashboard
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
FILE_PATH=
DB_SERVER=
DB_DATABASE=
```

- `FILE_PATH` — path to your spells JSON file (e.g. `spells.json`)
- `DB_SERVER` — your SQL Server instance name (e.g. `localhost` or `.\SQLEXPRESS`)
- `DB_DATABASE` — the name of your database

### 4. Set Up the Database

Run the SQL scripts in the following order in SQL Server Management Studio (SSMS) or Azure Data Studio:

**Tables (run all six in any order):**
- `sql/tables/create_fact_spells.sql`
- `sql/tables/create_dim_classes.sql`
- `sql/tables/create_dim_schools.sql`
- `sql/tables/create_dim_damage_types.sql`
- `sql/tables/create_bridge_spells_and_classes.sql`
- `sql/tables/create_bridge_spells_and_damage_types.sql`

**Foreign Keys (must run after all six tables above):**
- `sql/tables/add_foreign_keys.sql`

**Stored Procedures (run in any order):**
- `sql/stored_procedures/usp_insert_spell.sql`
- `sql/stored_procedures/usp_insert_spell_and_class.sql`
- `sql/stored_procedures/usp_insert_spell_and_damage_type.sql`

### 5. Add Your Spells JSON

A `test_data.json` file is included in the repo with 50 dummy spells for demonstration purposes. To get started quickly, set `FILE_PATH=test_data.json` in your `.env` file. Note that these are not real DnD spells — they exist purely to showcase the dashboard.

To use your own spells, replace `test_data.json` with your own file and update `FILE_PATH` accordingly. The file must be a JSON array where each element is a spell object. Required fields must be present on every spell; optional fields can be omitted.

**Required fields:**

| Field | Type | Description |
|---|---|---|
| `name` | string | Name of the spell |
| `level` | integer | Spell level (0 for cantrips, 1–9 for leveled spells) |
| `school` | string | School of magic (e.g. `"evocation"`, `"illusion"`) |
| `classes` | array of strings | Classes that can cast this spell (e.g. `["wizard", "sorcerer"]`) |
| `actionType` | string | Action cost — `"action"`, `"bonusAction"`, or `"reaction"` |
| `concentration` | boolean | Whether the spell requires concentration |
| `ritual` | boolean | Whether the spell can be cast as a ritual |
| `range` | string | Spell range (e.g. `"60 feet"`, `"Self"`, `"Touch"`) |
| `components` | array of strings | Components required — any combination of `"v"`, `"s"`, `"m"` |
| `duration` | string | How long the spell lasts (e.g. `"Instantaneous"`, `"up to 1 minute"`) |
| `description` | string | Full spell description |

**Optional fields:**

| Field | Type | Description |
|---|---|---|
| `material` | string | Description of the material component. To specify a GP cost, include a number followed by `GP` (e.g. `"a diamond worth 50+ GP"`). To flag the material as consumed on cast, include the word `consume` (e.g. `"which the spell consumes"`). |
| `higherLevelSlot` | string | Effect when cast using a higher-level spell slot |
| `cantripUpgrade` | string | How the cantrip scales at character levels 5, 11, and 17 |

**Example spell:**

```json
[
  {
    "name": "Searing Ray",
    "level": 1,
    "school": "evocation",
    "classes": ["sorcerer", "wizard"],
    "actionType": "action",
    "concentration": false,
    "ritual": false,
    "range": "90 feet",
    "components": ["v", "s"],
    "duration": "Instantaneous",
    "description": "You hurl a concentrated beam of fire at a creature within range. Make a ranged spell attack against the target. On a hit, the target takes 3d8 Fire damage.",
    "higherLevelSlot": "The damage increases by 1d8 for each spell slot level above 1."
  }
]
```

> **Note on descriptions:** `spellParser.py` derives several fields automatically from the description text. For saving throws to be detected, write them as `"<stat> saving throw"` (e.g. `"Dexterity saving throw"`). For damage to be detected, include a dice expression before the word damage (e.g. `"3d8 Fire damage"`). For half-damage on a successful save to be detected, include the phrase `"half as much damage"`. For damage type to be detected, make sure that damage is detected and that the damage type you want is in the hard-coded _damage_types enum in the spellParser.py file. You can edit the hard-coded _damage_types enum to remove or add damage types. You can also use modify the upload.py argument to use the --damageTypeOff argument to have all damage types be no damage type when inserting into the database.

## Running the Pipeline

```bash
python upload.py
```

This reads the spells JSON, parses each spell using `spellParser.py`, and inserts the results into SQL Server via the stored procedures.

## Power BI Dashboard

### Connecting to Your Database

1. Open `Spell_Visualizations_Template.pbix` in Power BI Desktop
2. Go to **Transform Data → Data Source Settings**
3. Update the server and database name to match your `.env` values
4. Click **Close** and hit **Refresh**

The dashboard expects the following tables in your database:

- `fact_spells`
- `bridge_spells_and_classes`
- `dim_classes`
- `dim_schools`

## Project Structure

```
DnD_Spell_Dashboard/
├── upload.py                          # Pipeline entry point
├── spellParser.py                     # Parses and enriches spell JSON
├── test_data.json                     # Dummy spells for demonstration
├── spells.json                        # Your spells data (not tracked in git)
├── .env                               # Environment variables (not tracked in git)
├── Spell_Visualizations_Template.pbix # Power BI dashboard template
└── sql/
    ├── tables/
    │   ├── create_fact_spells.sql
    │   ├── create_dim_classes.sql
    │   ├── create_dim_schools.sql
    │   ├── create_bridge_spells_and_classes.sql
    │   └── add_foreign_keys.sql
    └── stored_procedures/
        ├── usp_insert_spell.sql
        └── usp_insert_spell_and_class.sql
```
