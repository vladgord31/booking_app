import customtkinter as CTk
from PIL import Image, ImageTk
from views.login_view import LoginView


class LoadingScreen(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TicketHub")
        self.geometry("460x370")
        self.resizable(False, False)

        self.gif_path = "images/loading.gif"
        self.frames = []
        self.load_gif()

        self.gif_label = CTk.CTkLabel(self, text="")
        self.gif_label.place(x=0, y=0)  

        self.current_frame = 0
        self.animate_gif()

        self.after(10000, self.open_sign_in)

    def load_gif(self):
        try:
            gif = Image.open(self.gif_path)
            for frame in range(gif.n_frames):
                gif.seek(frame)
                resized_frame = gif.copy().resize(
                    (580, 470)
                )  
                self.frames.append(ImageTk.PhotoImage(resized_frame))
        except FileNotFoundError:
            print("GIF не знайдено. Перевірте шлях до файлу.")
            self.frames.append(
                ImageTk.PhotoImage(Image.new("RGB", (460, 370), "black"))
            )  

    def animate_gif(self):
        if self.frames:
            self.gif_label.configure(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.after(100, self.animate_gif)  

    def open_sign_in(self):
        self.destroy()
        main_window = LoginView()
        main_window.mainloop()
