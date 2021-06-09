from tkinter import *

from table import Table


class Rooms(Frame):
    def __init__(self, dba, parent=None):
        super().__init__(parent)

        self.dba = dba
        self.btn_clear = Button(self, text="Clear table", command=self.on_clear_table_click)
        self.btn_clear.pack(side=RIGHT, pady=5, padx=10)
        self.table = Table(self, dba.rooms_headings, ["123", "222"])
        self.table.pack(side=BOTTOM, pady=10, padx=10)

        self.left_frame = Frame(self)
        self.lbl_search = Label(self.left_frame, text="Enter room")
        self.lbl_search.pack()
        self.ent_search = Entry(self.left_frame)
        self.ent_search.pack(pady=10)
        self.btn_search = Button(self.left_frame, text="Search", command=self.on_search_click)
        self.btn_search.pack(side=RIGHT)
        self.btn_delete = Button(self.left_frame, text="Delete", command=self.on_delete_click)
        self.btn_delete.pack(side=LEFT)
        self.left_frame.pack(side=LEFT, padx=16)

        self.right_frame = Frame(self)

        self.btn_add = Button(self.right_frame, text="Add", command=self.on_add_click)
        self.btn_add.pack(side=BOTTOM, ipadx=56)

        self.price_frame = Frame(self.right_frame)
        self.lbl_price = Label(self.price_frame, text="Price per night")
        self.lbl_price.pack()
        self.ent_price = Entry(self.price_frame)
        self.ent_price.pack()
        self.price_frame.pack(side=RIGHT, pady=10, padx=10)

        self.room_frame = Frame(self.right_frame)
        self.lbl_room = Label(self.room_frame, text="Room")
        self.lbl_room.pack()
        self.ent_room = Entry(self.room_frame)
        self.ent_room.pack()
        self.room_frame.pack(side=RIGHT, pady=10, padx=10)

        self.right_frame.pack(side=RIGHT, padx=16)

    def update_table(self, data):
        if data is not None:
            self.table.update_table(data)

    def on_clear_table_click(self):
        self.update_table(self.dba.clear_rooms())

    def on_search_click(self):
        target = self.ent_search.get()
        if 0 < len(target) <= 4:
            self.update_table(self.dba.search_room(target))
        else:
            self.dba.error("Incorrect search data")

    def on_delete_click(self):
        target = self.ent_search.get()
        if 0 < len(target) <= 4:
            self.update_table(self.dba.delete_room(target))
        else:
            self.dba.error("Incorrect delete data")

    def on_add_click(self):
        room = self.ent_room.get()
        price = self.ent_price.get()
        if 0 < len(room) <= 4 and len(price) > 0:
            self.update_table(self.dba.add_room(room, int(price)))
        else:
            self.dba.error("Incorrect data")
