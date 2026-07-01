CREATE TABLE bridge_spells_and_damage_types (
	spell_id INT,
	damage_type_id INT,
	CONSTRAINT PK_spells_and_damage_types PRIMARY KEY (spell_id, damage_type_id)
)