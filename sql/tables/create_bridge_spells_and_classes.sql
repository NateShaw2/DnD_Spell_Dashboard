CREATE TABLE bridge_spells_and_classes (
	spell_id INT,
	class_id INT,
	CONSTRAINT PK_spells_and_classes PRIMARY KEY(spell_id, class_id)
)