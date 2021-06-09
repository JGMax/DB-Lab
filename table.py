from tkinter import *
from tkinter import ttk


class Table:
    # todo update table
    # todo popup menu listeners
    def __init__(self, parent, headings=tuple(), rows=tuple()):
        table = ttk.Treeview(parent, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        self.parent = parent
        self.selection = StringVar()

        self.popup = Menu(self.parent, tearoff=0)
        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, anchor=CENTER)
            self.popup.add_radiobutton(label="Edit " + head, command=self.edit, value=head,
                                       variable=self.selection)

        self.popup.add_command(label="Delete", command=self.edit)

        for row in rows:
            table.insert('', END, values=tuple(row))

        scrolltable = Scrollbar(parent, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)
        table.bind("<Button-3>", self.do_popup)
        self.table = table

    def do_popup(self, event):
        try:
            self.popup.selection = self.table.set(self.table.identify_row(event.y))
            self.popup.post(event.x_root, event.y_root)
        finally:
            self.popup.grab_release()

    def delete(self):
        #  todo delete row + update db
        for selection in self.table.selection():
            print(str(selection))

    def edit(self, *args):
        #  todo edit field + update db
        print(self.selection.get())
        print(self.popup.selection)

    def pack(self, *args, **kwargs):
        self.table.pack(*args, **kwargs)

    def update_table(self, data):
        for i, val in enumerate(data):
            data[i] = list(val.values())
        print(data)