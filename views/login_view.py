import customtkinter as CTk
from PIL import Image
from tkinter import messagebox
from database.database import Database
from views.register_view import RegistrView
from views.admin_view import AdminView
from views.main_view import App

class LoginView(CTk.CTk): 
    def __init__(self):
        super().__init__()

        self.title("Sign In")
        self.geometry("780x600")
        self.resizable(False, False)

        self.configure(fg_color="white") 
        self.tk_setPalette(background="white")  

        self.img = CTk.CTkImage(
            dark_image=Image.open("images/login.jpg"), size=(390, 600)
        )
        self.label_img = CTk.CTkLabel(
            master=self, text="", image=self.img
        ) 

        self.label_img.place(x=0, y=0)

        self.frame = CTk.CTkFrame(master=self, height=600, width=390, fg_color="white")
        self.frame.place(x=390, y=70)

        self.header1 = CTk.CTkLabel(
            master=self.frame,
            text="Welcome back!",
            font=("Arial", 32, "bold"),
            text_color="#78039b",
        )
        self.header1.place(x=25, y=0)

        self.header2 = CTk.CTkLabel(
            master=self.frame,
            text="Sign in to your account",
            font=("Arial", 13, "bold"),
            text_color="#272727",
        )
        self.header2.place(x=25, y=50)

        self.img_user = CTk.CTkImage(
            dark_image = Image.open("images/user.jpeg"), size=(16, 16)
        )
        self.label_img_user = CTk.CTkLabel(
            master=self.frame, text="", image=self.img_user
        )
        self.label_img_user.place(x=27, y=135)

        self.label_username = CTk.CTkLabel(
            master=self.frame,
            text="Username:",
            text_color="#78039b",
            font=("Arial", 14, "bold"),
        )
        self.label_username.place(x=47, y=135)

        self.username = CTk.CTkEntry(
            master=self.frame,
            width=325,
            height=35,
            fg_color="#ebebeb",
            text_color="black",
            border_width=2,
            border_color="#78039b",
            corner_radius=10,
        )
        self.username.place(x=25, y=160)

        self.img_password = CTk.CTkImage(
            dark_image = Image.open("images/password.jpeg"), size=(16, 16)
        )
        self.label_img_password = CTk.CTkLabel(
            master=self.frame, text="", image=self.img_password
        )
        self.label_img_password.place(x=27, y=215)

        self.label_password = CTk.CTkLabel(
            master=self.frame,
            text="Password:",
            text_color="#78039b",
            font=("Arial", 14, "bold"),
        )
        self.label_password.place(x=47, y=215)
        self.password = CTk.CTkEntry(
            master=self.frame,
            width=325,
            height=35,
            fg_color="#ebebeb",
            text_color="black",
            border_width=2,
            border_color="#78039b",
            show="*",
            corner_radius=10,
        )
        self.password.place(x=25, y=240)

        self.button = CTk.CTkButton(
            master=self.frame,
            width=325,
            height=35,
            text="Login",
            text_color="white",
            font=("Arial", 14, "bold"),
            fg_color="#78039b",
            border_width=0,
            hover_color="#78039b",
            cursor="hand2",
            command=self.sign_in,
            corner_radius=10,
        )
        self.button.place(x=25, y=324)

        self.link = CTk.CTkLabel(
            master=self.frame,
            text="Don't have an account?",
            font=("Arial", 11, "bold"),
            text_color="#272727",
        )
        self.link.place(x=27, y=364)

        self.sign_up = CTk.CTkButton(
            master=self.frame,
            text="Register",
            height=35,
            width=40,
            text_color="#78039b",
            fg_color="white",
            cursor="hand2",
            hover_color="white",
            font=("Arial", 11, "bold"),
            command=self.open_register_view,
        )
        self.sign_up.place(x=166, y=361)

    def sign_in(self):
        username = self.username.get()
        password = self.password.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return

        db = Database("users.db")
        db.create_table_users()

        user = db.fetch_user(username, password)
        role = db.fetch_user_role(username)
        db.close()

        if user:
            messagebox.showinfo("Login Success", "Welcome back!")
            if role and role[0] == "admin":
                self.open_admin_view()
            else:
                self.open_main_view()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def open_register_view(self):
        self.destroy()
        register_view = RegistrView()
        register_view.mainloop()

    def open_main_view(self):
        self.destroy()
        main_view = App()
        main_view.mainloop()

    def open_admin_view(self):
        self.destroy()
        admin_view = AdminView()
        admin_view.mainloop()
