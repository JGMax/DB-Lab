from tkinter import *

from database import Database
from error_ui import Error
from login_ui import Login


class App(Tk):
    def __init__(self):
        super().__init__()
        self.columnconfigure([0, 1], weight=1, minsize=75)
        self.rowconfigure(0, weight=1, minsize=50)
        self.wm_minsize(250, 50)
        self.title("Hotel database")
        self.db = None
        self.btn_connection = Button(self, text="Connect", command=self.on_connection_click)
        self.btn_connection.pack()

    def on_connection_click(self):
        if self.db is not None:
            self.disconnect()
            self.btn_connection["text"] = "Connect"
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
            # todo set table
            self.btn_connection["text"] = "Disconnect"
            return True
        except Exception as e:
            print(str(e))
            self.error(str(e))
            return False

    def error(self, msg):
        error = Error(msg=msg, parent=self)
        error.grab_set()
