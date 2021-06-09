from tkinter import *
from tkinter.ttk import Notebook

from database import Database
from edit_ui import Edit
from error_ui import Error
from login_ui import Login
from rooms_ui import Rooms


class App(Tk):
    def __init__(self):
        super().__init__()
        # todo add orders frame
        self.rooms_headings = ["id", "room_number", "night_price"]
        self.columnconfigure([0, 1], weight=1, minsize=75)
        self.rowconfigure(0, weight=1, minsize=50)
        self.wm_minsize(250, 50)
        self.title("Hotel database")
        self.db = None

        self.note = Notebook(self)
        self.rooms = Rooms(dba=self, parent=self.note)
        self.orders = Frame(self.note)
        self.note.add(self.rooms, text="Rooms")
        self.note.add(self.orders, text="Orders")
        self.note.pack()

        self.btn_connection = Button(self, text="Connect", command=self.on_connection_click)
        self.btn_connection.pack(side=RIGHT, padx=10, ipadx=10, pady=10)
        self.btn_clear = Button(self, text="Clear all tables", command=self.on_clear_all_click)
        self.btn_clear.pack(side=RIGHT, padx=10, pady=10)
        self.btn_drop = Button(self, text="Delete database", command=self.on_delete_database_click)
        self.btn_drop.pack(side=RIGHT, padx=10, pady=10)

    def on_delete_database_click(self):
        if self.db is None:
            self.error("Database is disconnected")
            return
        self.db.drop()
        self.btn_connection["text"] = "Connect"
        self.db = None

    def on_clear_all_click(self):
        if self.db is None:
            self.error("Database is disconnected")
            return
        self.db.clear_all()

    def on_connection_click(self):
        if self.db is not None:
            self.disconnect()
            self.btn_connection["text"] = "Connect"
            self.db = None
        else:
            self.open_login()

    def open_login(self):
        login = Login(app=self, parent=self)
        login.grab_set()

    def disconnect(self):
        if self.db is not None:
            self.db.disconnect()
            self.db = None

    def connect(self, host, name, port, login, password, s_file):
        if host == '' or name == '' or port == '' or login == '' or password == '':
            self.error("Empty fields")
            return False
        try:
            self.db = Database(host, name, port, login, password, s_file)
            self.rooms.update_table(self.db.get_rooms())
            # todo update orders
            self.btn_connection["text"] = "Disconnect"
            return True
        except Exception as e:
            print(str(e))
            self.error(str(e))
            return False

    def error(self, msg):
        error = Error(msg=msg, parent=self)
        error.grab_set()

    def get_rooms(self):
        if self.db is not None:
            return self.db.get_rooms()
        else:
            self.error("Database is disconnected")
            return None

    def clear_rooms(self):
        if self.db is not None:
            return self.db.clear_rooms()
        else:
            self.error("Database is disconnected")
            return None

    def search_room(self, target):
        if self.db is not None:
            return self.db.search_room(target)
        else:
            self.error("Database is disconnected")
            return None

    def delete_room(self, target):
        if self.db is not None:
            return self.db.search_room(target)
        else:
            self.error("Database is disconnected")
            return None

    def add_room(self, room, price):
        if self.db is not None:
            return self.db.add_room(room, price)
        else:
            self.error("Database is disconnected")
            return None

    def update_item_room(self, id, changing_column, new_value):
        if self.db is not None:
            return self.db.edit_item_room(id, changing_column, new_value)
        else:
            self.error("Database is disconnected")
            return None

    def delete_item_room(self, id):
        if self.db is not None:
            return self.db.delete_item_room(id)
        else:
            self.error("Database is disconnected")
            return None

    def edit(self, data_type, values, parent_tab):
        if self.db is not None:
            edit = Edit(edit_type=data_type, old_values=values, parent_tab=parent_tab, parent=self)
            edit.grab_set()
        else:
            self.error("Database is disconnected")
            return None

    def update_values_room(self, new_values):
        if self.db is not None:
            return self.db.update_item_room(new_values)
        else:
            self.error("Database is disconnected")
            return None

