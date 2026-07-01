-- =============================================
-- Create date: 6/30/2026
-- Description:	Inserts bridge data
-- =============================================

CREATE OR ALTER PROCEDURE usp_insert_bridge_spell_and_damage_type
	@spell_name VARCHAR(255),
	@damage_type_name VARCHAR(255)
AS 
BEGIN
	SET NOCOUNT ON;

	DECLARE @spell_id INT;
	SELECT @spell_id = spell_id FROM fact_spells WHERE name = @spell_name;

	IF @spell_id IS NULL
	BEGIN
		RAISERROR('No matching spell found for %s', 16, 1, @spell_name);
		RETURN;
	END

	DECLARE @damage_type_id INT;
	SELECT @damage_type_id = damage_type_id FROM dim_damage_types WHERE name = @damage_type_name;

	IF @damage_type_id IS NULL
	BEGIN
		RAISERROR('No matching class found for %s', 16, 1, @damage_type_name);
		RETURN;
	END

	IF NOT EXISTS (SELECT 1 FROM bridge_spells_and_damage_types WHERE spell_id = @spell_id AND damage_type_id = @damage_type_id)
	BEGIN
		INSERT INTO bridge_spells_and_damage_types(
			spell_id,
			damage_type_id
		)
		VALUES (
			@spell_id,
			@damage_type_id
		);
	
	END
END
GO