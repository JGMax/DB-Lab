from tkinter import *
from tkinter.ttk import Notebook

from database import Database
from edit_ui import Edit
from error_ui import Error
from login_ui import Login
from orders_ui import Orders
from rooms_ui import Rooms


class App(Tk):
    def __init__(self):
        super().__init__()
        self.rooms_headings = ["id", "room_number", "night_cost"]
        self.orders_headings = ["id", "room_id", "night_count", "arrival_time", "total_cost"]

        self.columnconfigure([0, 1], weight=1, minsize=75)
        self.rowconfigure(0, weight=1, minsize=50)
        self.wm_minsize(1220, 405)
        self.wm_maxsize(1220, 405)
        self.title("Hotel database")
        self.db = None

        self.note = Notebook(self)
        self.rooms = Rooms(dba=self, parent=self.note)
        self.orders = Orders(dba=self, parent=self.note)
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
        self.rooms.update_table(None)
        self.orders.update_table(None)

    def on_clear_all_click(self):
        if self.db is None:
            self.error("Database is disconnected")
            return
        try:
            self.db.clear_all()
            self.rooms.update_table(self.db.get_rooms())
            self.orders.update_table(self.db.get_orders())
        except Exception as e:
            self.error(str(e))

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
            self.rooms.update_table(None)
            self.orders.update_table(None)

    def connect(self, host, name, port, login, password, s_file):
        if host == '' or name == '' or port == '' or login == '' or password == '':
            self.error("Empty fields")
            return False
        try:
            self.db = Database(host, name, port, login, password, s_file)
            self.rooms.update_table(self.db.get_rooms())
            self.orders.update_table(self.db.get_orders())
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
            try:
                return self.db.get_rooms()
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def get_orders(self):
        if self.db is not None:
            try:
                return self.db.get_orders()
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def clear_rooms(self):
        if self.db is not None:
            try:
                self.db.clear_rooms()
                self.rooms.update_table(self.db.get_rooms())
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")

    def clear_orders(self):
        if self.db is not None:
            try:
                self.db.clear_orders()
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")

    def search_room(self, target):
        if self.db is not None:
            try:
                return self.db.search_room(target)
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def search_orders(self, target):
        if self.db is not None:
            try:
                return self.db.search_orders(target)
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def delete_room(self, target):
        if self.db is not None:
            try:
                self.db.delete_room(target)
                self.rooms.update_table(self.db.get_rooms())
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def delete_orders(self, target):
        if self.db is not None:
            try:
                self.db.delete_orders(target)
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def add_room(self, room, price):
        if self.db is not None:
            try:
                self.db.add_room(room, price)
                self.rooms.update_table(self.db.get_rooms())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def add_orders(self, room_id, night_count):
        if self.db is not None:
            try:
                self.db.add_orders(room_id, night_count)
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def delete_item_room(self, id):
        if self.db is not None:
            try:
                self.db.delete_item_room(id)
                self.rooms.update_table(self.db.get_rooms())
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def delete_item_orders(self, id):
        if self.db is not None:
            try:
                self.db.delete_item_orders(id)
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
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
            try:
                self.db.update_item_room(new_values)
                self.rooms.update_table(self.db.get_rooms())
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None

    def update_values_orders(self, new_values):
        if self.db is not None:
            try:
                self.db.update_item_orders(new_values)
                self.orders.update_table(self.db.get_orders())
            except Exception as e:
                self.error(str(e))
        else:
            self.error("Database is disconnected")
            return None
