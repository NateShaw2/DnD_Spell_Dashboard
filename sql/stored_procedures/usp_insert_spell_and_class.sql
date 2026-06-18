-- =============================================
-- Create date: 6/17/2026
-- Description:	Inserts bridge data
-- =============================================

CREATE OR ALTER PROCEDURE usp_insert_bridge_spell_and_class
	@spell_name VARCHAR(255),
	@class_name VARCHAR(255)
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

	DECLARE @class_id INT;
	SELECT @class_id = class_id FROM dim_classes WHERE name = @class_name;

	IF @class_id IS NULL
	BEGIN
		RAISERROR('No matching class found for %s', 16, 1, @class_name);
		RETURN;
	END

	IF NOT EXISTS (SELECT 1 FROM bridge_spells_and_classes WHERE spell_id = @spell_id AND class_id = @class_id)
	BEGIN
		INSERT INTO bridge_spells_and_classes(
			spell_id,
			class_id
		)
		VALUES (
			@spell_id,
			@class_id
		);
	
	END
END
GO