import sqlite3
from tkinter import messagebox
import customtkinter as CTk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from matplotlib import pyplot as plt
from database.database import Database


class AdminView(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TicketHub - Admin")
        self.geometry("1440x720")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.db = Database("users.db")

        self.navigation_frame = CTk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = CTk.CTkLabel(
            self.navigation_frame,
            text="TicketHub Admin",
            compound="left",
            font=("Arial", 24, "bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = CTk.CTkButton(
            self.navigation_frame,
            text="Admin Panel",
            corner_radius=0,
            height=40,
            font=("Arial", 14, "bold"),
            border_spacing=10,
            fg_color="transparent",
            text_color=("#5e027b", "#78039b"),
            hover_color=("gray70", "gray30"),
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.stats_button = CTk.CTkButton(
            self.navigation_frame,
            text="Statistics",
            corner_radius=0,
            height=40,
            font=("Arial", 14, "bold"),
            border_spacing=10,
            fg_color="transparent",
            text_color=("#5e027b", "#78039b"),
            hover_color=("gray70", "gray30"),
            command=self.stats_button_event,
        )
        self.stats_button.grid(row=2, column=0, sticky="ew")

        self.add_ticket_button = CTk.CTkButton(
            self.navigation_frame,
            text="Add Ticket",
            corner_radius=0,
            height=40,
            font=("Arial", 14, "bold"),
            border_spacing=10,
            fg_color="transparent",
            text_color=("#78039b", "#78039b"),
            hover_color=("gray70", "gray30"),
            command=self.add_ticket_button_event,
        )
        self.add_ticket_button.grid(row=3, column=0, sticky="ew")

        self.logout_button = CTk.CTkButton(
            self.navigation_frame,
            text="Logout",
            height=40,
            corner_radius=0,
            font=("Arial", 14, "bold"),
            border_spacing=10,
            fg_color="transparent",
            text_color=("#78039b", "#78039b"),
            hover_color=("gray70", "gray30"),
            command=self.logout,
        )
        self.logout_button.grid(row=9, column=0, sticky="ew")

        self.appearance_mode_menu = CTk.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            fg_color="#78039b",
            button_color="#78039b",
            button_hover_color="#5e027b",
            text_color="white",
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        self.home_frame = CTk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.stats_frame = CTk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.add_ticket_frame = CTk.CTkFrame(
            self, corner_radius=0, 
            fg_color="transparent",
        )

        self.select_frame_by_name("home")

        self.protocol("WM_DELETE_WINDOW", self.on_close)  

    def select_frame_by_name(self, name):
        if name == "home":
            self.load_home_frame()
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "stats":
            self.load_stats_frame()
            self.stats_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.stats_frame.grid_forget()
        if name == "add_ticket":
            self.load_add_ticket_frame()
            self.add_ticket_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.add_ticket_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def stats_button_event(self):
        self.select_frame_by_name("stats")

    def add_ticket_button_event(self):
        self.select_frame_by_name("add_ticket")

    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    def load_home_frame(self):
        for widget in self.home_frame.winfo_children():
            widget.destroy()

        self.home_frame.grid_columnconfigure(0, weight=1)

        users = self.db.cursor.execute("SELECT * FROM users").fetchall()

        for i, user in enumerate(users):
            user_frame = CTk.CTkFrame(self.home_frame, fg_color="lightgray")
            user_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            user_frame.grid_columnconfigure(0, weight=1)

            title_label = CTk.CTkLabel(
                user_frame,
                text=f"Username: {user[1]}",
                text_color="#78039b",
                font=("Arial", 14, "bold"),
            )
            title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            description_label = CTk.CTkLabel(
                user_frame,
                text=f"Email: {user[3]}, Role: {user[4]}",
                text_color="#78039b",
                font=("Arial", 14, "bold"),
            )
            description_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    def load_stats_frame(self):
        self.visits_db = Database("visits.db")
        self.visits_db.reset_weekly_data()

        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        self.title_label = CTk.CTkLabel(
            self.stats_frame, text="Статистика відвідувань", font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=10)

        conn = sqlite3.connect("visits.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT day, visit_count 
            FROM visits 
            ORDER BY 
                CASE day
                    WHEN 'Mon' THEN 1
                    WHEN 'Tue' THEN 2
                    WHEN 'Wed' THEN 3
                    WHEN 'Thu' THEN 4
                    WHEN 'Fri' THEN 5
                    WHEN 'Sat' THEN 6
                    WHEN 'Sun' THEN 7
                END
            """
        )
        data = cursor.fetchall()

        conn.commit()
        conn.close()

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        visits = [0] * 7

        for day, visit_count in data:
            day = day[:3]
            if day in days:
                day_index = days.index(day)
                visits[day_index] = visit_count
            else:
                print(f"Некоректний день: {day}")

        current_theme = CTk.get_appearance_mode()
        bg_color = "#333333" if current_theme == "Dark" else "white"
        text_color = "white" if current_theme == "Dark" else "black"

        fig, ax = plt.subplots(figsize=(12, 8), facecolor=bg_color)
        ax.plot(
            days,
            visits,
            marker="o",
            linestyle="-",
            color="#78039b",
            markersize=8,
            linewidth=2,
        )

        ax.set_facecolor(bg_color)
        ax.set_title(
            "Щоденні відвідування", fontsize=16, fontweight="bold", color="#78039b"
        )
        ax.set_xlabel("Дні тижня", fontsize=14, fontweight="bold", color=text_color)
        ax.set_ylabel(
            "Кількість відвідувань", fontsize=14, fontweight="bold", color=text_color
        )
        ax.tick_params(colors=text_color)

        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        canvas.draw()

        plt.close(fig)

        self.stats_frame.grid_rowconfigure(2, weight=1, minsize=400)
        self.stats_frame.grid_columnconfigure(0, weight=1)

    def load_add_ticket_frame(self):
        for widget in self.add_ticket_frame.winfo_children():
            widget.destroy()

        self.add_ticket_frame.grid_columnconfigure(0, weight=1)
        self.add_ticket_frame.grid_columnconfigure(1, weight=1)
        self.add_ticket_frame.grid_columnconfigure(2, weight=1)

        title_frame = CTk.CTkFrame(
            self.add_ticket_frame, 
            corner_radius=0, 
            fg_color="transparent",
        )
        title_frame.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

        left_frame = CTk.CTkFrame(
            self.add_ticket_frame, 
            corner_radius=0, 
            fg_color="transparent"
        )
        left_frame.grid(row=1, column=0, padx=120, pady=60, sticky="nsew")

        right_frame = CTk.CTkFrame(
            self.add_ticket_frame, 
            corner_radius=0, 
            fg_color="transparent",
        )
        right_frame.grid(row=1, column=1, padx=10, pady=60, sticky="nsew")

        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)

        label_add_new_ticket = CTk.CTkLabel(
            title_frame,
            font=("Arial", 24),
            text="Add new ticket",
            text_color="#78039b",
        )
        label_add_new_ticket.grid(row=0, column=1, pady=20, sticky="nsew")

        title_frame.grid_columnconfigure(1, weight=1)

        label_price = CTk.CTkLabel(
            left_frame,
            text="Price:",
            font=("Arial", 16),
            text_color=("#78039b", "#78039b"),
        )
        label_price.grid(row=1, column=0, sticky="w", padx=20)

        price_entry = CTk.CTkEntry(
            left_frame,
            corner_radius=10,
            fg_color=("white", "#ebebeb"),
            font=("Arial", 16),
            width=400,
            height=40,
            text_color="black",
            border_width=2,
            border_color="#78039b",
        )
        price_entry.grid(row=2, column=0, pady=5)

        label_departure_date = CTk.CTkLabel(
            left_frame,
            text="Departure Date:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_departure_date.grid(row=3, column=0, sticky="w", padx=20)

        departure_date_entry = CTk.CTkEntry(
            left_frame,
            corner_radius=10,
            width=400,
            height=40,
            border_width=2,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
        )
        departure_date_entry.grid(row=4, column=0, pady=5)

        label_arrival_date = CTk.CTkLabel(
            left_frame,
            text="Arrival Date:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_arrival_date.grid(row=5, column=0, sticky="w", padx=20)

        arrival_date_entry = CTk.CTkEntry(
            left_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_width=2,
            border_color="#78039b",
        )
        arrival_date_entry.grid(row=6, column=0, pady=5)

        label_description = CTk.CTkLabel(
            left_frame,
            text="Description:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_description.grid(row=7, column=0, sticky="w", padx=20)

        description_entry = CTk.CTkEntry(
            left_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
            border_width=2,
        )
        description_entry.grid(row=8, column=0, pady=5)

        label_departure_city = CTk.CTkLabel(
            left_frame,
            text="Departure City:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_departure_city.grid(row=9, column=0, sticky="w", padx=20)

        departure_city_entry = CTk.CTkEntry(
            left_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
            border_width=2,
        )
        departure_city_entry.grid(row=10, column=0, pady=5)

        label_arrival_city = CTk.CTkLabel(
            right_frame,
            text="Arrival City:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_arrival_city.grid(row=1, column=1, sticky="w", padx=20)

        arrival_city_entry = CTk.CTkEntry(
            right_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
            border_width=2,
        )
        arrival_city_entry.grid(row=2, column=1, pady=5)

        label_departure_time = CTk.CTkLabel(
            right_frame,
            text="Departure_time:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_departure_time.grid(row=3, column=1, sticky="w", padx=20)

        departure_time_entry = CTk.CTkEntry(
            right_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
            border_width=2,
        )
        departure_time_entry.grid(row=4, column=1, pady=5)

        label_arriaval_time = CTk.CTkLabel(
            right_frame,
            text="Arrival_time:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_arriaval_time.grid(row=5, column=1, sticky="w", padx=20)

        arrival_time_entry = CTk.CTkEntry(
            right_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
            border_width=2,
        )
        arrival_time_entry.grid(row=6, column=1, pady=5)

        label_photo_path = CTk.CTkLabel(
            right_frame,
            text="Photo Path:",
            font=("Arial", 16),
            text_color="#78039b",
        )
        label_photo_path.grid(row=7, column=1, sticky="w", padx=20)

        photo_entry = CTk.CTkEntry(
            right_frame,
            corner_radius=10,
            width=400,
            height=40,
            text_color="black",
            font=("Arial", 16),
            fg_color=("white", "#ebebeb"),
            border_color="#78039b",
            border_width=2,
        )
        photo_entry.grid(row=8, column=1, pady=5)

        save_button = CTk.CTkButton(
            right_frame,
            text="Save Ticket",
            font=("Arial", 16, "bold"),
            width=400,
            height=40,
            corner_radius=10,
            fg_color="#78039b",
            hover_color="#78039b",
            command=lambda: self.save_ticket(
                price_entry.get(),
                departure_date_entry.get(),
                arrival_date_entry.get(),
                description_entry.get(),
                departure_time_entry.get(),
                arrival_time_entry.get(),
                departure_city_entry.get(),
                arrival_city_entry.get(),
                photo_entry.get(),
            ),
        )
        save_button.grid(row=10, column=1, pady=35)

    def save_ticket(
        self,
        price,
        departure_date,
        arrival_date,
        departure_time,
        arrival_time,
        description,
        departure_city,
        arrival_city,
        photo,
    ):
        try:
            db = Database("tickets.db")
            db.create_table_tickets()
            db.insert_ticket(
                float(price),
                departure_date,
                arrival_date,
                departure_time,
                arrival_time,
                description,
                departure_city,
                arrival_city,
                photo,
            )
            messagebox.showinfo("Success", "Ticket added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add ticket: {e}")

    def logout(self):
        self.destroy()
        from views.login_view import LoginView

        LoginView().mainloop()

    def on_close(self):
        self.quit()  
        self.destroy()  
