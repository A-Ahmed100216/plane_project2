import pyodbc
import pandas
from aircraft_class import Aircraft

class Flight_Trip(Aircraft):
    def __init__(self):
        super().__init__()

    def create_table(self):
        self.cursor.execute("CREATE TABLE Flight_Trip (Flight_ID INT NOT NULL IDENTITY(1,1) PRIMARY KEY, craft_id INT NOT NULL REFERENCES aircraft(craft_id) , Destination VARCHAR(100), Duration_hrs INT, Scheduled_Date VARCHAR(50),Scheduled_Time VARCHAR(50));")
        self.connection.commit()

    def view_table(self):
        flights_table = self.cursor.execute("SELECT * FROM Flight_Trip").fetchall()
        return flights_table

    def existing_flights(self):
        self.cursor.execute("INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (1, 'Marbella', 2, '12/12/2019', '12:00');")
        self.cursor.execute("INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (2, 'St Lucia', 8, '14/12/2019', '01:00');")
        self.cursor.execute(
            "INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (4, 'Los Angeles', 10, '14/05/2019', '08:00');")
        self.cursor.execute(
            "INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (3, 'Antigua', 9, '06/06/2019', '10:00');")

        self.connection.commit()

    def add_flight(self):
        craft_id = input("Please enter the aircraft ID number for this flight ==> ")
        destination = input("Where are you flying to? ==> ")
        duration = int(input("How many hours is this flight? ==> "))
        date = input("Please enter the date of this flight(dd/mm/yyy) ==> ")
        time = input("What time is the flight?(hh:mm) ==> ")
        self.cursor.execute(f"INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time ) VALUES ('{craft_id}', '{destination}', '{duration}', '{date}','{time}');")
        self.connection.commit()
        print(f"Success. Flight to {destination} added")

    def change_plane(self):
        flight_id=input("Please select the flight id where you wish to assign a new aircraft: ")
        new_craft_id=input("Please enter the new craft id you wish to assign")
        # confirm=input(f"Are you sure you would like to change {flight_id} to a new aircraft,{new_craft_id}? y/n")
        return self.cursor.execute(f"UPDATE Flight_Trip SET craft_id={new_craft_id} WHERE Flight_ID={flight_id}")





# if __name__=="__main__":
#     test = Flight_Trip()
    # test.create_table()
    # test.existing_flights()
    # test.add_flight()
    # print(test.view_table())