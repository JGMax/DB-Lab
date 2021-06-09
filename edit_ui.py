from tkinter import *


class Edit(Toplevel):
    def __init__(self, edit_type, old_values, parent_tab, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.edit_type = edit_type
        self.old_values = old_values
        self.parent_tab = parent_tab

        self.wm_minsize(250, 70)
        self.title("Edit " + edit_type)
        self.edit = Entry(self)
        self.edit.insert(END, old_values[edit_type])
        self.edit.pack(pady=4)
        self.cancel = Button(self, text="Cancel", command=self.destroy)
        self.cancel.pack(side=RIGHT, pady=8, padx=4)
        self.update = Button(self, text="Update", command=self.on_update_click)
        self.update.pack(side=RIGHT, padx=4)

    def on_update_click(self):
        val = self.edit.get()
        if self.edit_type == 'room_number':
            if 0 < len(val) <= 4:
                self.old_values[self.edit_type] = val
                self.parent_tab.update_item(self.old_values)
                self.destroy()
                del self
            else:
                self.parent.error("Incorrect data")
        else:
            if len(val) > 0:
                self.old_values[self.edit_type] = val
                self.parent_tab.update_item(self.old_values)
                self.destroy()
                del self
            else:
                self.parent.error("Incorrect data")

