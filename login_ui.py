from tkinter import *
from tkinter.filedialog import askopenfilename


class Login(Toplevel):
    def __init__(self, app=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.title("Login")
        self.wm_minsize(290, 215)
        self.wm_maxsize(290, 215)

        frm_form = Frame(self, relief=SUNKEN, borderwidth=3)
        frm_form.pack()

        frame1 = Frame(
            master=frm_form
        )
        frame1.grid(row=0, column=0, padx=8, pady=4)

        frame2 = Frame(
            master=frm_form
        )
        frame2.grid(row=0, column=1, padx=8, pady=4)

        self.lbl_host = Label(master=frame1, text="Host")
        self.lbl_host.pack()
        self.ent_host = Entry(master=frame1)
        self.ent_host.pack(pady=8)

        self.lbl_login = Label(master=frame2, text="Login")
        self.lbl_login.pack()
        self.ent_login = Entry(master=frame2)
        self.ent_login.pack(pady=8)

        self.lbl_db_name = Label(master=frame1, text="Database name")
        self.lbl_db_name.pack()
        self.ent_db_name = Entry(master=frame1)
        self.ent_db_name.pack(pady=8)

        self.lbl_password = Label(master=frame2, text="Password")
        self.lbl_password.pack()
        self.ent_password = Entry(master=frame2, show="*")
        self.ent_password.pack(pady=8)

        self.lbl_port = Label(master=frame1, text="Port")
        self.lbl_port.pack()
        self.ent_port = Entry(master=frame1)
        self.ent_port.pack(pady=8)

        self.lbl_structure = Label(master=frame2, text="Structure file path (.sql)")
        self.lbl_structure.pack()
        self.ent_structure = Entry(master=frame2)
        self.ent_structure.pack(pady=8)
        self.ent_structure.bind("<Button-1>", self.on_structure_click)

        frm_buttons = Frame(self)
        frm_buttons.pack(fill=X, ipadx=5, ipady=5)

        self.btn_connect = Button(master=frm_buttons, text="Connect", command=self.on_connect_click)
        self.btn_cancel = Button(master=frm_buttons, text="Cancel", command=self.out)

        self.btn_cancel.pack(side=RIGHT, padx=10, ipadx=10)
        self.btn_connect.pack(side=RIGHT, ipadx=10)

    def out(self):
        self.destroy()

    def on_structure_click(self, event):
        if self.ent_structure.get() == "":
            filepath = askopenfilename(
                filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
            )
            if not filepath:
                return
            self.ent_structure.insert(END, filepath)

    def on_connect_click(self):
        host = self.ent_host.get()
        login = self.ent_login.get()
        name = self.ent_db_name.get()
        password = self.ent_password.get()
        port = self.ent_port.get()
        s_file = self.ent_structure.get()
        success = self.app.connect(host, name, port, login, password, s_file)
        if success:
            self.out()
