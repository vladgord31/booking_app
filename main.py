import customtkinter as CTk
from views.loading_screen import LoadingScreen

if __name__ == "__main__":
    CTk.set_appearance_mode("dark")
    CTk.set_default_color_theme("blue")

    app = LoadingScreen()
    app.iconbitmap("images/logo.ico")  
    app.mainloop()
