CREATE TABLE city (
	id UUID NOT NULL, 
	slug VARCHAR(20) NOT NULL, 
	full_name VARCHAR(60) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT id_startswith_type_prefix CHECK (CAST(id AS char(1)) = '1'), 
	UNIQUE (slug)
)


CREATE TABLE company (
	id UUID NOT NULL, 
	full_name VARCHAR(60) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT id_startswith_type_prefix CHECK (CAST(id AS char(1)) = '2')
)


CREATE TABLE city_company (
	city_id UUID NOT NULL, 
	company_id UUID NOT NULL, 
	company_slug VARCHAR(20) NOT NULL, 
	PRIMARY KEY (city_id, company_id), 
	UNIQUE (city_id, company_slug), 
	FOREIGN KEY(city_id) REFERENCES city (id) ON DELETE RESTRICT, 
	FOREIGN KEY(company_id) REFERENCES company (id) ON DELETE CASCADE
)


CREATE TABLE route (
	id UUID NOT NULL, 
	name VARCHAR(12) NOT NULL, 
	number VARCHAR(6), 
	city_id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT id_startswith_type_prefix CHECK (CAST(id AS char(1)) = '3'), 
	FOREIGN KEY(city_id) REFERENCES city (id) ON DELETE CASCADE
)


CREATE TABLE stop_area (
	id UUID NOT NULL, 
	city_id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT id_startswith_type_prefix CHECK (CAST(id AS char(1)) = '5'), 
	FOREIGN KEY(city_id) REFERENCES city (id) ON DELETE CASCADE
)


CREATE TABLE company_route (
	company_id UUID NOT NULL, 
	route_id UUID NOT NULL, 
	PRIMARY KEY (company_id, route_id), 
	FOREIGN KEY(company_id) REFERENCES company (id) ON DELETE CASCADE, 
	FOREIGN KEY(route_id) REFERENCES route (id) ON DELETE CASCADE
)


CREATE TABLE stop (
	id UUID NOT NULL, 
	full_name VARCHAR(100) NOT NULL, 
	short_name VARCHAR(60) NOT NULL, 
	stop_area_id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT id_startswith_type_prefix CHECK (CAST(id AS char(1)) = '4'), 
	FOREIGN KEY(stop_area_id) REFERENCES stop_area (id) ON DELETE CASCADE
)


CREATE TABLE route_stop (
	route_id UUID NOT NULL, 
	stop_id UUID NOT NULL, 
	leg_index SMALLINT NOT NULL CHECK (leg_index >= 0), 
	leg_distance INTEGER NOT NULL CHECK (leg_distance >= 0), 
	PRIMARY KEY (route_id, stop_id), 
	UNIQUE (route_id, stop_id, leg_index, leg_distance), 
	FOREIGN KEY(route_id) REFERENCES route (id) ON DELETE CASCADE, 
	FOREIGN KEY(stop_id) REFERENCES stop (id) ON DELETE RESTRICT
)
