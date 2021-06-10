
CREATE OR REPLACE FUNCTION create_table() RETURNS void AS $$

CREATE TABLE rooms (
	id SMALLSERIAL NOT NULL PRIMARY KEY,
	room_number VARCHAR(4) NOT NULL DEFAULT '',
	night_cost INTEGER NOT NULL CHECK(night_cost >= 0)
);
CREATE TABLE orders (
	id SMALLSERIAL NOT NULL PRIMARY KEY,
	room_id SMALLINT REFERENCES rooms(id) ON DELETE CASCADE,
	night_count SMALLINT NOT NULL CHECK(night_count >= 0),
	arrival_time TIMESTAMP NOT NULL DEFAULT current_timestamp(0),
	total_cost INTEGER CHECK(total_cost >= 0) DEFAULT 0
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

CREATE TRIGGER update_data_trigger_insert
BEFORE INSERT ON orders
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

CREATE OR REPLACE FUNCTION clear_all_tables()
RETURNS VOID AS $$ TRUNCATE rooms CASCADE;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION get_orders_by_room(in room VARCHAR(4)) RETURNS JSON AS $$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  	'id', orders.id,
	'room_id', orders.room_id,
	'night_count', orders.night_count,
	'arrival_time', orders.arrival_time,
	'total_cost', orders.total_cost
  ))FROM orders JOIN rooms on orders.room_id = rooms.id WHERE rooms.room_number=room) ;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_rooms_by_room(in room VARCHAR(4)) RETURNS JSON AS $$
BEGIN
  RETURN (SELECT json_agg(json_build_object(
  	'id', rooms.id,
	'room_number', rooms.room_number,
	'night_cost', rooms.night_cost
  ))FROM rooms WHERE rooms.room_number=room) ;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_rooms_by_room(in room VARCHAR(4)) RETURNS void AS $$
BEGIN
  DELETE FROM rooms WHERE room_number = room;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_rooms_by_id(in room_id_ integer) RETURNS void AS $$
BEGIN
  DELETE FROM rooms WHERE id = room_id_;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_orders_by_id(in orders_id_ integer) RETURNS void AS $$
BEGIN
  DELETE FROM orders WHERE id = orders_id_;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_room(in room_number_ VARCHAR(4), in night_cost_ integer) RETURNS void AS $$
BEGIN
	INSERT INTO rooms(room_number, night_cost)
	VALUES (room_number_, night_cost_);
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_order(in room_id_ integer, in night_count_ integer) RETURNS void AS $$
BEGIN
	INSERT INTO orders(room_id, night_count)
	VALUES (room_id_, night_count_);
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_room(in room_id integer, in room_number_ VARCHAR(4), in night_cost_ integer) RETURNS void AS $$
BEGIN
	UPDATE rooms SET(room_number, night_cost)=(room_number_, night_cost_)
	WHERE rooms.id = room_id;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_order(in order_id_ integer, in room_id_ integer, in arrival_time_ TIMESTAMP, in night_count_ integer) RETURNS void AS $$
BEGIN
	UPDATE orders SET(room_id, arrival_time, night_count)=(room_id_, arrival_time_ , night_count_)
	WHERE orders.id = order_id_;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION clear_orders_tables() RETURNS void AS $$
	TRUNCATE orders;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION delete_orders_by_room(in room VARCHAR(4)) RETURNS void AS $$
BEGIN
	DELETE FROM orders WHERE orders.room_id=(SELECT id FROM rooms WHERE room_number = room);
END
$$ LANGUAGE plpgsql;

--------------------------------------------------------------