import customtkinter as CTk
import os
from PIL import Image
from models.ticket import Ticket
from database.database import Database
from tkinter import messagebox  # Import messagebox to show a confirmation message


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TicketHub")
        self.geometry("1440x720")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.db = Database("tickets.db")
        self.visits_db = Database("visits.db")
        self.visits_db.update_visit_count_by_day()

        self.navigation_frame = CTk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = CTk.CTkLabel(
            self.navigation_frame,
            text="  TicketHub",
            compound="left",
            text_color="#78039b",
            font=("Arial", 21, "bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = CTk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Home",
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            text_color=("#78039b", "#78039b"),
            hover_color=("gray70", "gray30"),
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.tickets_button = CTk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Tickets",
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            text_color=("#78039b", "#78039b"),
            hover_color=("gray70", "gray30"),
            command=self.tickets_button_event,
        )
        self.tickets_button.grid(row=2, column=0, sticky="ew")

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
        self.logout_button.grid(row=6, column=0, sticky="ew")

        self.appearance_mode_menu = CTk.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            fg_color="#78039b",
            button_color="#78039b",
            button_hover_color="#5e027b",
            text_color="white",
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        self.home_frame = CTk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.tickets_frame = CTk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.tickets_frame.grid_columnconfigure(0, weight=1)

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.tickets_button.configure(
            fg_color=("gray75", "gray25") if name == "tickets" else "transparent"
        )

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "tickets":
            self.load_tickets()
            self.tickets_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tickets_frame.grid_forget()

    def load_tickets(self):
        for widget in self.tickets_frame.winfo_children():
            widget.destroy()

        tickets = self.db.cursor.execute("SELECT * FROM tickets").fetchall()

        for i, ticket in enumerate(tickets):
            ticket_frame = CTk.CTkFrame(self.tickets_frame, fg_color="lightgray")
            ticket_frame.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            ticket_frame.grid_columnconfigure(1, weight=1)

            title_label = CTk.CTkLabel(
                ticket_frame,
                text=f"{ticket[5]} to {ticket[6]}",
                text_color="#78039b",
                font=("Arial", 16, "bold"),
            )
            title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            description_label = CTk.CTkLabel(
                ticket_frame,
                text=f"Departure: {ticket[2]}, Arrival: {ticket[3]}\nPrice: ${ticket[1]}",
                text_color="#78039b",
                font=("Arial", 12, "bold"),
            )
            description_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            buy_button = CTk.CTkButton(
                ticket_frame,
                text="Buy",
                command=lambda t=ticket: self.buy_ticket(t[0]),
            )
            buy_button.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="e")

    def buy_ticket(self, ticket_id):
        # Show success message
        messagebox.showinfo(
            "Purchase Successful", "You have successfully bought the ticket."
        )

        # Hide purchased ticket
        self.db.cursor.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
        self.db.connection.commit()

        # Reload tickets to reflect changes
        self.load_tickets()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def tickets_button_event(self):
        self.select_frame_by_name("tickets")

    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    def logout(self):
        self.destroy()
        from views.login_view import LoginView

        LoginView().mainloop()
