from tkinter import *


class Error(Toplevel):
    def __init__(self, msg, parent=None):
        super().__init__(parent)
        self.wm_minsize(250, 70)
        self.title("Error")
        self.error = Label(self, text=msg)
        self.error.pack()
        self.cancel = Button(self, text="Cancel", command=self.destroy)
        self.cancel.pack(pady=8)
