CREATE TABLE dim_damage_types (
	damage_type_id INT IDENTITY(1,1) PRIMARY KEY,
	name VARCHAR(255) UNIQUE
)