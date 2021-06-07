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
            self.init_structure()
        else:
            connection.close()
            self.connect()

    def connect(self):
        self.connection = psycopg2.connect(self.conn_str)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def init_structure(self):
        f = open(self.structure_file)
        if self.cursor is not None:
            self.cursor.execute(f.read())
        f.close()

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
