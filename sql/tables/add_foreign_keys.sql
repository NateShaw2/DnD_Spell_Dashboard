ALTER TABLE fact_spells
ADD CONSTRAINT FK_spell_school FOREIGN KEY (school_id) REFERENCES dim_schools(school_id);

ALTER TABLE bridge_spells_and_classes
ADD 
	CONSTRAINT FK_spell FOREIGN KEY (spell_id) REFERENCES fact_spells(spell_id),
	CONSTRAINT FK_class FOREIGN KEY (class_id) REFERENCES dim_classes(class_id);

ALTER TABLE bridge_spells_and_damage_types
ADD
	CONSTRAINT FK_spell_bridge_spells_and_damage_types FOREIGN KEY (spell_id) REFERENCES fact_spells(spell_id),
	CONSTRAINT FK_damage_type FOREIGN KEY (damage_type_id) REFERENCES dim_damage_types(damage_type_id);