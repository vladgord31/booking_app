import sqlite3


class Ticket:
    def __init__(
        self,
        id,
        price,
        departure_date,
        arrival_date,
        description,
        departure_city,
        arrival_city,
        departure_time,
        arrival_time,
        photo,
    ):
        self.id = id
        self.price = price
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.description = description
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.photo = photo

    @staticmethod
    def get_tickets(
        id,
        price,
        departure_date,
        arrival_date,
        description,
        departure_city,
        arrival_city,
        departure_time,
        arrival_time,
        photo=None,
    ):
        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        query = """
            SELECT * FROM tickets WHERE 
                price = ? AND 
                departure_date = ? AND 
                arrival_date = ? AND 
                description = ? AND 
                departure_city = ? AND 
                arrival_city = ? AND 
                departure_time = ? AND
                arrival_time = ? AND
                number = ?
        """

        params = [
            price,
            departure_date,
            arrival_date,
            description,
            departure_city,
            arrival_city,
            departure_time,
            arrival_time,
        ]

        if photo is not None:
            query += " AND photo = ?"
            params.append(photo)

        cursor.execute(query, tuple(params))
        tickets = cursor.fetchall()
        conn.close()
        return tickets

    @staticmethod
    def get_ticket(
        price,
        departure_date,
        arrival_date,
        description,
        departure_city,
        arrival_city,
        departure_time,
        arrival_time,
        photo=None,
    ):
        conn = sqlite3.connect("tickets.db")
        cursor = conn.cursor()

        query = """
            SELECT * FROM tickets WHERE 
                price = ? AND 
                departure_date = ? AND 
                arrival_date = ? AND 
                description = ? AND 
                departure_city = ? AND 
                arrival_city = ? AND
                departure_time = ? AND
                arrival_time = ? AND
        """

        params = [
            price,
            departure_date,
            arrival_date,
            description,
            departure_city,
            arrival_city,
            departure_time,
            arrival_time,
        ]

        if photo is not None:
            query += " AND photo = ?"
            params.append(photo)

        cursor.execute(query, tuple(params))
        ticket = cursor.fetchone()
        conn.close()
        return ticket
