from db_connection import DB_Connection
import pandas as pd
from aircraft_class import Aircraft

class Booking(DB_Connection):

    def __init__(self):
        super().__init__()
        self.ticket_price = 100
        self.total_tickets = 0


    def available_seats(self):
        print("We have the following flight trips available:  ")
        query=(f"SELECT Flight_Trip.destination as Destination, aircraft.Capacity as Seats_Available , aircraft.craft_id, Flight_Trip.flight_id FROM aircraft INNER JOIN Flight_Trip ON aircraft.craft_id=Flight_Trip.craft_id")
        exported_data = pd.read_sql_query(query, self.connection)
        df_2 = pd.DataFrame(exported_data)
        print(df_2)

    def booking(self):
        # Ask user to input flight id of the flight they wish to book
        flight_id=input("Please enter the flight id of the destination you wish to travel to: ")
        # Determine seats available on flight based on the craft id associated with the flight trip.
        seats_available=(self.cursor.execute(f"SELECT aircraft.Capacity FROM aircraft INNER JOIN Flight_Trip ON aircraft.craft_id=Flight_Trip.craft_id where Flight_Trip.flight_id={flight_id} and aircraft.capacity!=0 ").fetchone())[0]
        # Is the ticket valid, is passport and visa valid for destination person is travelling to.
        check = input("Is the ticket, passport and visa valid for travel to destination? (Y/N)    ")
        # If check fails, prompted to enter a new destination.
        if check.lower() == "n":
            print("You cannot travel to this destination, please select a new destination")
            return self.booking()
        # Set tickets and order total to zero.
        tickets_ordered = 0
        order_total = 0
        # Use try,except to counter errors if invalid data entered in user prompts
        try:
            adult_tickets = int(input("How many adult tickets would you like to purchase?    "))
            child_tickets = int(input("How many child tickets (ages 2-14) would you like to purchase?    "))
            lap_child_tickets = int(input("How many lap child tickets (ages 0-2) would you like to purchase?    "))
        except ValueError as err:
            print("Please Enter a Valid Number")
            return
        else:
            pass

        # If num of tickets greater than 0, calculate cost and add to order total. Add seats to seat total.
        if adult_tickets > 0:
            order_total += (adult_tickets * self.ticket_price)
            tickets_ordered += adult_tickets
            self.total_tickets += adult_tickets
        # Repeat for child but charge 75% of cost for children.
        if child_tickets > 0:
            order_total += (child_tickets * (self.ticket_price * 0.75))
            tickets_ordered += child_tickets
            self.total_tickets += child_tickets
        # Repeat for lap_child, charging 30% of original price.
        if lap_child_tickets > 0:
            order_total += (lap_child_tickets * (self.ticket_price * 0.3))
            tickets_ordered += lap_child_tickets
            self.total_tickets += lap_child_tickets
        # If tickets ordered exceeds number of seats, raise error
        try:
            if tickets_ordered > seats_available:
                raise ValueError
        except ValueError:
            print("You have ordered too many tickets... Please try again")
            return
        else:
            pass
        # Print statement notifying user of how many tickets they have ordered
        print(f"\nYou have ordered {tickets_ordered} tickets: \n"
              f"{adult_tickets} Adult tickets \n"
              f"{child_tickets} Child tickets \n"
              f"{lap_child_tickets} Lap Child tickets \n"
              f"Your order total is £{order_total} \n")

        # Ask user to confirm their order
        confirmation = input("Would you like to continue with the purchase? (Y/N)    ")
        # If they confirm, directed to seat_counter and order_details function.
        if confirmation == "y":
            self.seat_counter(adult_tickets, child_tickets,seats_available)
            self.order_details(flight_id, adult_tickets, child_tickets, lap_child_tickets, order_total)
        else:
            return

    # Seat counter (See how many seats are available. If seat is sold, subtract from seats available before.)
    def seat_counter(self, adult_tickets, child_tickets,seats_available):
        if adult_tickets > 0:
            seats_available -= adult_tickets
        if child_tickets > 0:
            seats_available -= child_tickets
            return f"There are {seats_available} seats remaining on the flight"

    # Order details method, prints details in formatted way.
    def order_details(self, flight_id, adult_tickets, child_tickets, lap_child_tickets, order_total):
        # Determine the destination from the flight id
        destination=(self.cursor.execute(f"SELECT destination FROM Flight_Trip WHERE flight_id={flight_id}").fetchone())[0]
        # Insert into Booking_details table
        self.cursor.execute(f"""INSERT INTO Booking_details(Flight_ID, Infant_tickets, Child_tickets, Adult_tickets, Total_unit_price)
                            VALUES('{flight_id}', '{lap_child_tickets}', '{child_tickets}', '{adult_tickets}', '{order_total}')""")
        self.connection.commit()
        # Display to console using print statements
        print(" -------------------------------------------------------------")
        print(" Thank you for purchasing. Your order details are as follows: ")
        print(" -------------------------------------------------------------")
        print(f"Flight ID :                 {flight_id}                      ")
        print(f"Flight Destination :        {destination}                    ")
        print(f"Adult Tickets:              {adult_tickets}                  ")
        print(f"Child Tickets :             {child_tickets}                  ")
        print(f"Infant Tickets :            {lap_child_tickets}              ")
        print("--------------------------------------------------------------")


# Test - Instantiate class
# test=Booking()
# test.booking()

