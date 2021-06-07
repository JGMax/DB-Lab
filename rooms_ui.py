from tkinter import *

from table import Table


class Rooms(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        #  todo get headings + update table
        #  todo click listeners
        #  todo add clear table button
        self.table = Table(self, ["aaa", "gg"], ["fa","f","f","f","f","f","f","f","f","f","a","f","f"])
        self.table.pack(side=BOTTOM, pady=10, padx=10)

        self.left_frame = Frame(self)
        self.lbl_search = Label(self.left_frame, text="Enter room")
        self.lbl_search.pack()
        self.ent_search = Entry(self.left_frame)
        self.ent_search.pack(pady=10)
        self.btn_search = Button(self.left_frame, text="Search")
        self.btn_search.pack(side=RIGHT)

        self.btn_delete = Button(self.left_frame, text="Delete")
        self.btn_delete.pack(side=LEFT)
        self.left_frame.pack(side=RIGHT, padx=16)

        self.right_frame = Frame(self)

        self.btn_add = Button(self.right_frame, text="Add")
        self.btn_add.pack(side=BOTTOM)

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

