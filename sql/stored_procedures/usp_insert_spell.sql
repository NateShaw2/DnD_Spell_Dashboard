-- =============================================
-- Create date: 6/17/2026
-- Description:	Inserts spell data
-- =============================================

CREATE OR ALTER PROCEDURE usp_insert_spell
	@name VARCHAR(255),
	@level TINYINT,
	@school_name VARCHAR(255),
	@action_type VARCHAR(255),
	@is_concentration BIT,
	@is_ritual BIT,
	@casting_time VARCHAR(255) = NULL,
	@range VARCHAR(255),
	@require_visual_component BIT,
	@require_somatic_component BIT,
	@require_material_component BIT,
	@components VARCHAR(6),
	@duration VARCHAR(255),
	@description VARCHAR(MAX),
	@materials VARCHAR(MAX) = NULL,
	@cantrip_upgrade VARCHAR(MAX) = NULL,
	@higher_level_slot VARCHAR(MAX) = NULL,
	@material_cost INT,
	@does_spell_consume BIT,
	@saving_throw_type VARCHAR(255),
	@is_half_damage_on_success BIT,
	@does_damage BIT,
	@is_exclusive BIT
AS
BEGIN
	SET NOCOUNT ON;

	DECLARE @school_id INT;
	SELECT @school_id = school_id FROM dim_schools WHERE name = @school_name;

	IF @school_id IS NULL
	BEGIN
		RAISERROR('No matching school found for %s', 16, 1, @school_name);
		RETURN;
	END

	IF NOT EXISTS (SELECT 1 FROM fact_spells WHERE name = @name)
	BEGIN
        INSERT INTO fact_spells (
			name,
            level,
            school_id,
            action_type,
            is_concentration,
            is_ritual,
            casting_time,
            range,
            require_visual_component,
            require_somatic_component,
            require_material_component,
			components,
            duration,
            description,
            materials,
            cantrip_upgrade,
            higher_level_slot,
			upgrade_info,
            material_cost,
            does_spell_consume,
            saving_throw_type,
            is_half_damage_on_success,
			does_damage,
            is_exclusive
		)
		VALUES (
			@name,
            @level,
            @school_id,
            @action_type,
            @is_concentration,
            @is_ritual,
            @casting_time,
            @range,
            @require_visual_component,
            @require_somatic_component,
            @require_material_component,
			@components,
            @duration,
            @description,
            @materials,
            @cantrip_upgrade,
            @higher_level_slot,
			COALESCE(@cantrip_upgrade, @higher_level_slot),
            @material_cost,
            @does_spell_consume,
            @saving_throw_type,
            @is_half_damage_on_success,
			@does_damage,
            @is_exclusive
		);

	END
END
GO