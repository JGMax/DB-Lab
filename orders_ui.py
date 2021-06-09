from tkinter import *

from table import Table


class Orders(Frame):
    def __init__(self, dba, parent=None):
        super().__init__(parent)

        self.dba = dba
        self.btn_clear = Button(self, text="Clear table", command=self.on_clear_table_click)
        self.btn_clear.pack(side=RIGHT, pady=5, padx=10)
        self.table = Table(self, dba.orders_headings)
        self.table.pack(side=BOTTOM, pady=10, padx=10)

        self.left_frame = Frame(self)
        self.lbl_search = Label(self.left_frame, text="Enter room id")
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

        self.nights_frame = Frame(self.right_frame)
        self.ent_nights = Label(self.nights_frame, text="Nights count")
        self.ent_nights.pack()
        self.ent_nights = Entry(self.nights_frame)
        self.ent_nights.pack()
        self.nights_frame.pack(side=RIGHT, pady=10, padx=10)

        self.room_frame = Frame(self.right_frame)
        self.lbl_room = Label(self.room_frame, text="Room id")
        self.lbl_room.pack()
        self.ent_room = Entry(self.room_frame)
        self.ent_room.pack()
        self.room_frame.pack(side=RIGHT, pady=10, padx=10)

        self.right_frame.pack(side=RIGHT, padx=16)

    def delete_item(self, id):
        self.update_table(self.dba.delete_item_orders(id))

    def edit_item(self, type, values):
        self.dba.edit(type, values, self)

    def update_item(self, new_values):
        self.update_table(self.dba.update_values_orders(new_values))

    def update_table(self, data):
        if data is not None:
            self.table.update_table(data)

    def on_clear_table_click(self):
        self.update_table(self.dba.clear_orders())

    def on_search_click(self):
        target = self.ent_search.get()
        if len(target) > 0:
            self.update_table(self.dba.search_orders(target))
        else:
            self.dba.error("Incorrect search data")

    def on_delete_click(self):
        target = self.ent_search.get()
        if len(target) > 0:
            self.update_table(self.dba.delete_orders(target))
        else:
            self.dba.error("Incorrect delete data")

    def on_add_click(self):
        room_id = self.ent_room.get()
        nights = self.ent_nights.get()
        if len(room_id) > 0 and len(nights) > 0:
            self.update_table(self.dba.add_orders(room_id, int(nights)))
        else:
            self.dba.error("Incorrect data")

