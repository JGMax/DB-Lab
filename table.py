from tkinter import *
from tkinter import ttk


class Table:
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
            if head != 'id' and head != "total_cost":
                self.popup.add_radiobutton(label="Edit " + head, command=self.edit, value=head,
                                           variable=self.selection)

        self.popup.add_command(label="Delete", command=self.delete)

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
        if self.popup.selection:
            self.parent.delete_item(self.popup.selection["id"])

    def edit(self, *args):
        if self.popup.selection:
            self.parent.edit_item(self.selection.get(), self.popup.selection)

    def pack(self, *args, **kwargs):
        self.table.pack(*args, **kwargs)

    def update_table(self, data):
        self.table.delete(*self.table.get_children())
        if data:
            for i, val in enumerate(data):
                self.table.insert('', END, values=tuple(val.values()))
