import json

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql


class Database:
    def __init__(self, host, name, port, login, password, structure_file):
        self.structure_file = structure_file
        self.name = name
        self.password = password
        self.login = login
        self.port = port
        self.host = host
        self.connection = None
        self.cursor = None
        self.conn_str = "host=" + host + " port=" + port \
                        + " dbname=" + name + " user=" + login + " password=" + password
        self.conn_str_postgres = "host=" + host + " port=" + port \
                                 + " dbname=postgres" + " user=" + login + " password=" + password
        self.create()

    def create(self):
        connection = psycopg2.connect(self.conn_str_postgres)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (self.name, ))
        if not cursor.fetchone():
            self.test_file()
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.name)))
            connection.close()
            self.connect()
            self.init_structure()
        else:
            connection.close()
            self.connect()

    def connect(self):
        self.connection = psycopg2.connect(self.conn_str)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def test_file(self):
       open(self.structure_file, encoding='utf-8')

    def init_structure(self):
        with open(self.structure_file, encoding='utf-8') as f:
            if self.cursor is not None:
                self.cursor.execute(f.read())

    def drop(self):
        if self.connection is not None:
            self.connection.close()
        conn = psycopg2.connect(self.conn_str_postgres)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(self.name)))
        conn.close()
        del self

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
        del self

    def clear_all(self):
        self.cursor.callproc("clear_all_tables")

    def get_rooms(self):
        self.cursor.callproc("get_rooms")
        fetch = self.cursor.fetchone()[0]
        if fetch is not None:
            return json.loads(str(fetch).replace("'", '"'))

    def clear_rooms(self):
        self.cursor.callproc("clear_all_tables")

    def search_room(self, target):
        self.cursor.callproc("get_rooms_by_room", (target, ))
        fetch = self.cursor.fetchone()[0]
        if fetch is not None:
            return json.loads(str(fetch).replace("'", '"'))

    def delete_room(self, target):
        self.cursor.callproc("delete_rooms_by_room", (target, ))

    def add_room(self, room, night_cost):
        self.cursor.callproc("add_room", (room, night_cost, ))

    def update_item_room(self, new_data):
        id = new_data["id"]
        room_number = new_data["room_number"]
        night_cost = new_data["night_cost"]
        self.cursor.callproc("update_room", (id, room_number, night_cost, ))

    def delete_item_room(self, id):
        self.cursor.callproc("delete_rooms_by_id", (id, ))

    def get_orders(self):
        self.cursor.callproc("get_orders")
        fetch = self.cursor.fetchone()[0]
        if fetch is not None:
            return json.loads(str(fetch).replace("'", '"'))

    def clear_orders(self):
        print("Clear orders")
        return None

    def search_orders(self, target):
        self.cursor.callproc("get_orders_by_room", (target, ))
        fetch = self.cursor.fetchone()[0]
        if fetch is not None:
            return json.loads(str(fetch).replace("'", '"'))

    def delete_orders(self, target):
        print("Delete orders " + target)
        return None

    def add_orders(self, room_id, nights):
        self.cursor.callproc("add_order", (room_id, nights, ))

    def update_item_orders(self, new_data):
        id = new_data["id"]
        room_id = new_data["room_id"]
        night_count = new_data["night_count"]
        arrival_time = new_data["arrival_time"]
        self.cursor.callproc("update_order", (int(id), int(room_id), arrival_time, int(night_count), ))

    def delete_item_orders(self, id):
        self.cursor.callproc("delete_orders_by_id", (id, ))
