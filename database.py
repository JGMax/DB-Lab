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
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.name)))
            connection.close()
            self.connect()
        else:
            connection.close()
            self.connect()

    def connect(self):
        self.connection = psycopg2.connect(self.conn_str)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def test_file(self):
        try:
            with open(self.structure_file, encoding='utf-8'):
                return True
        except IOError as e:
            print(str(e))
            return False

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
        print("Clear all")
        return None

    def get_rooms(self):
        self.cursor.callproc("get_rooms")
        return json.loads(str(self.cursor.fetchone()[0]).replace("'", '"'))

    def clear_rooms(self):
        print("Clear room")
        return None

    def search_room(self, target):
        print("Search room " + target)
        return None

    def delete_room(self, target):
        print("Delete room " + target)
        return None

    def add_room(self, room, night_cost):
        print("Add room " + room + " " + str(night_cost))
        return None

    def update_item_room(self, new_data):
        print("Item updated room " + str(new_data))
        return None

    def delete_item_room(self, id):
        print("delete item room " + id)
        return None

    def get_orders(self):
        self.cursor.callproc("get_orders")
        return json.loads(str(self.cursor.fetchone()[0]).replace("'", '"'))

    def clear_orders(self):
        print("Clear orders")
        return None

    def search_orders(self, target):
        print("Search orders " + target)
        return None

    def delete_orders(self, target):
        print("Delete orders " + target)
        return None

    def add_orders(self, room_id, nights):
        print("Add orders " + room_id + " " + str(nights))
        return None

    def update_item_orders(self, new_data):
        print("Item updated orders " + str(new_data))
        return None

    def delete_item_orders(self, id):
        print("delete item orders " + id)
        return None
