CREATE TABLE bridge_spells_and_schools (
	spell_id INT,
	school_id INT,
	CONSTRAINT PK_spells_and_schools PRIMARY KEY(spell_id, school_id)
)