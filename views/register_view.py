import customtkinter as CTk
from PIL import ImageTk, Image
from tkinter import messagebox
from database.database import Database

class RegistrView(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sign up")
        self.geometry("780x600")
        self.resizable(False, False)

        self.configure(fg_color="white")
        self.tk_setPalette(background="white")

        self.img = CTk.CTkImage(
            dark_image=Image.open("images/login.jpg"), size=(390, 600)
        )
        self.img_label = CTk.CTkLabel(master=self, text="", image=self.img)

        self.img_label.place(x=390, y=0)

        self.frame = CTk.CTkFrame(master=self, height=600, width=390, fg_color="white")
        self.frame.place(x=0, y=20)

        self.header1 = CTk.CTkLabel(
            master=self.frame,
            text="Register form",
            font=("Arial", 32, "bold"),
            text_color="#78039b",
        )
        self.header1.place(x=25, y=20)

        self.header2 = CTk.CTkLabel(
            master=self.frame,
            text="Sign up for free",
            font=("Arial", 13, "bold"),
            text_color="#272727",
        )
        self.header2.place(x=25, y=66)

        self.img_username = CTk.CTkImage(
            dark_image=Image.open("images/user.jpeg"), size=(16, 16)
        )
        self.label_img_username = CTk.CTkLabel(
            master=self.frame, text="", image=self.img_username
        )
        self.label_img_username.place(x=27, y=135)

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
            border_width=2,
            text_color="black",
            border_color="#78039b",
            corner_radius=10,
        )
        self.username.place(x=25, y=160)

        self.img_email = CTk.CTkImage(
            dark_image=Image.open("images/email.jpeg"), size=(16, 16)
        )
        self.label_img_email = CTk.CTkLabel(
            master=self.frame, text="", image=self.img_email
        )
        self.label_img_email.place(x=27, y=210)

        self.label_email = CTk.CTkLabel(
            master=self.frame,
            text="Email:",
            text_color="#78039b",
            font=("Arial", 14, "bold"),
        )
        self.label_email.place(x=47, y=210)

        self.email = CTk.CTkEntry(
            master=self.frame,
            width=325,
            height=35,
            fg_color="#ebebeb",
            border_width=2,
            text_color="black",
            border_color="#78039b",
            corner_radius=10,
        )
        self.email.place(x=25, y=235)

        self.img_password = CTk.CTkImage(
            dark_image=Image.open("images/password.jpeg"), size=(16, 16)
        )
        self.label_img_password = CTk.CTkLabel(
            master=self.frame, text="", image=self.img_password
        )
        self.label_img_password.place(x=27, y=285)

        self.label_password = CTk.CTkLabel(
            master=self.frame,
            text="Password:",
            font=("Arial", 14, "bold"),
            text_color="#78039b",
        )
        self.label_password.place(x=47, y=285)

        self.password = CTk.CTkEntry(
            master=self.frame,
            width=325,
            height=35,
            fg_color="#ebebeb",
            border_width=2,
            border_color="#78039b",
            text_color="black",
            show="*",
            corner_radius=10,
        )
        self.password.place(x=25, y=310)

        self.img_confirm_password = CTk.CTkImage(
            dark_image=Image.open("images/password.jpeg"), size=(16, 16)
        )
        self.label_img_confirm_password = CTk.CTkLabel(
            master=self.frame, text="", image=self.img_confirm_password
        )
        self.label_img_confirm_password.place(x=27, y=360)

        self.label_confirm_password = CTk.CTkLabel(
            master=self.frame,
            text="Confirm password:",
            text_color="#78039b",
            font=("Arial", 14, "bold"),
        )
        self.label_confirm_password.place(x=47, y=360)

        self.confirm_password = CTk.CTkEntry(
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
        self.confirm_password.place(x=25, y=385)

        self.button = CTk.CTkButton(
            master=self.frame,
            width=325,
            height=35,
            text="Register",
            text_color="white",
            cursor="hand2",
            font=("Arial", 14, "bold"),
            fg_color="#78039b",
            border_width=0,
            hover_color="#78039b",
            command=self.register_user,
            corner_radius=10,
        )

        self.button.place(x=25, y=465)

        self.label_link = CTk.CTkLabel(
            master=self.frame,
            text="Your account already exist?",
            text_color="#272727",
            font=("Arial", 11, "bold"),
        )
        self.label_link.place(x=25, y=505)

        self.label_sign_in = CTk.CTkButton(
            master=self.frame,
            text="Login",
            height=35,
            width=30,
            text_color="#78039b",
            fg_color="white",
            hover_color="white",
            cursor="hand2",
            border_width=0,
            font=("Arial", 11, "bold"),
            corner_radius=10,
            command=self.open_sign_in,
        )
        self.label_sign_in.place(x=183, y=501.5)

    def register_user(self):
        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()

        if not username or not email or not password or not confirm_password:
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return
        elif password != confirm_password:
            messagebox.showerror("Input Error", "Passwords do not match!")
            return
        elif len(username) < 3 or len(password) < 6:
            messagebox.showerror(
                "Input Error",
                "Username must be at least 3 characters and password at least 6 characters!",
            )
            return

        db = Database("users.db")
        db.create_table_users()  

        try:
            db.insert_user(username, password, email)
            messagebox.showinfo("Success", "Registration successful!")
            self.open_sign_in()  
        except ValueError as e:
            messagebox.showerror("Registration Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            db.close()

    def open_sign_in(self):
        from views.login_view import LoginView

        self.destroy()
        main_window = LoginView()
        main_window.mainloop()
