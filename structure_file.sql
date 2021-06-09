
CREATE OR REPLACE FUNCTION create_table() RETURNS void AS $$

CREATE TABLE rooms (
	id SMALLSERIAL NOT NULL PRIMARY KEY,
	room_number VARCHAR(4) NOT NULL DEFAULT '',
	night_cost INTEGER NOT NULL CHECK(night_cost >= 0)
);
CREATE TABLE orders (
	id SMALLSERIAL NOT NULL PRIMARY KEY,
	room_id SMALLINT REFERENCES rooms(id) ON DELETE CASCADE,
	night_count INTEGER NOT NULL CHECK(night_count >= 0),
	arrival_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	total_cost INTEGER NOT NULL CHECK(total_cost >= 0)
);
CREATE UNIQUE INDEX room_number_idx ON rooms(room_number);
CREATE INDEX room_id_idx ON orders(room_id);
	
$$ LANGUAGE SQL;

SELECT create_table();

-------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_data() RETURNS trigger AS $$
BEGIN

NEW.total_cost = NEW.night_count * (SELECT night_cost FROM rooms WHERE id = NEW.room_id); 

RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


DROP TRIGGER IF EXISTS update_data_trigger on orders;

CREATE TRIGGER update_data_trigger
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE PROCEDURE update_data();

-------------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_rooms()
RETURNS JSON AS
$$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  'id', rooms.id,
  'room_number', rooms.room_number,
  'night_cost', rooms.night_cost
  )) FROM rooms);
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_orders()
RETURNS JSON AS
$$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  	'id', orders.id,
	'room_id', orders.room_id,
	'night_count', orders.night_count,
	'arrival_time', orders.arrival_time,
	'total_cost', orders.total_cost
  )) FROM orders);
END
$$ LANGUAGE plpgsql;

--------------------------------------------------------------

INSERT INTO rooms(room_number, night_cost)
VALUES ('N001', 150), ('N002', 300), ('N003', 400);

INSERT INTO orders(room_id, arrival_time, night_count, total_cost)
VALUES (1, '2004-10-19 10:23:54', 1, 0), (2, '2004-10-19 10:23:54', 2, 0)