#  Import relevant modules
import pandas as pd
import hashlib
from db_connection import DB_Connection
from booking_class import Booking
from flight_trip_class import Flight_Trip
from customers_class import Customer
from aircraft_class import Aircraft
from admin_class import Admin
from employees_class import Employees

class User_functions(DB_Connection):
    def __init__(self):
        super().__init__()
        self.functions = ["Create Flight Trip", "Add Passengers to flight trip", "Assign Plane", "Book Flight",
                          "Generate Flight Attendees", "Logout"]

    def login(self):
        # check if input is correct
        while True:
            username=input("Please enter your username:  ")
            password=input("Please enter your password:  ")
            encodedpass=hashlib.md5(password.encode()).hexdigest()
            exists=self.cursor.execute(f"SELECT * FROM [admin] WHERE username='{username}'and password='{encodedpass}'").fetchall()
            if exists:
                return self.user_interface()
            else:
                print("Invalid password or username. Please try again")

    def user_interface(self):
        print("Welcome to BADA Airlines!")
        user_input = input("              Menu            \n"
                           "-------------------------------\n"
                           "1. Create a flight trip \n"
                           "2. Add Passengers to flight trip\n"
                           "3. Assign Plane \n"
                           "4. Book Flight \n"
                           "5. Generate Flight Attendees \n"
                           "6. Admin \n"
                           "7. Log Out\n")

        if user_input == "1":
            trip=Flight_Trip()
            print("We have the following flight aircraft available:  ")
            exported_data = pd.read_sql_query('SELECT * FROM aircraft', self.connection)
            df_1 = pd.DataFrame(exported_data)
            print(df_1)
            trip.add_flight()
            print("Success")
            return self.user_interface()

        elif user_input == "2":
            print("We have the following flight trips available:  ")
            exported_data = pd.read_sql_query('SELECT Flight_ID, Destination FROM Flight_Trip', self.connection)
            df_2 = pd.DataFrame(exported_data)
            print(df_2)
            flight_id=input("Please enter the flight id you wish to add a passenger to:   ")
            in_db = self.cursor.execute(f"SELECT * FROM Flight_trip WHERE Flight_ID='{flight_id}'").fetchall()
            if not in_db:
                return "invalid input"
            passport_number=input("Please enter passport number:  ")
            first_name=input("Please enter  first name:   ")
            surname=input("Please enter last name:   ")
            tax_number=input("Please enter tax number:  ")
            gender = input("Please enter gender:  ")
            boarded_flight=input("Has the customer boarded the flight? 1=Yes 0=No  ")
            customer = Customer(passport_number, first_name,surname,tax_number)
            customer.add_to_customer_table(passport_number, first_name, surname,tax_number, flight_id, gender, boarded_flight)
            print("Success")
            return self.user_interface()


        elif user_input == "3":
            flight=Flight_Trip()
            print("We have the following crafts available in our fleet:  ")
            exported_data = pd.read_sql_query('SELECT * FROM aircraft', self.connection)
            df_2 = pd.DataFrame(exported_data)
            print(df_2)
            flight.change_plane()
            print("Success")
            return self.user_interface()



        elif user_input == "4":
            book = Booking()
            book.available_seats()
            book.booking()
            return self.user_interface()

        elif user_input== "5":
            self.generate_attendees()
            return self.user_interface()

        elif user_input == "6":
            return self.admin_menu()

        elif user_input=="7":
            exit()
        else:
            print("Invalid input")


    def admin_menu(self):
        admin = Admin()
        ask = input("          Menu       \n"
                    "------------------------\n"
                    "1. Create a new user \n"
                    "2. Add employee \n"
                    "3. Add new aircraft \n"
                    "4. Go back to main menu \n")
        if ask == "1":
            admin.create_user_login()
            "Success!!"
            return self.admin_menu()

        elif ask == "2":
            flight_id = input("Please enter your flight id   ")
            passport_number = input("Please enter your passport number    ")
            first_name = input("What is your first name?    ")
            surname = input("What is your surname?    ")
            gender = input("What is your gender?     ")
            occupation = input("What is your role within the company?    ")
            employee = Employees(passport_number, first_name, surname, gender, occupation)
            employee.add_to_employees_table(passport_number, first_name, surname, gender, occupation, flight_id)
            print("Success!")
            return self.admin_menu()

        elif ask=="3":
            admin.add_new_aircraft()
            print("Success!")
            return self.admin_menu()
        elif ask == "4":
            return self.user_interface()
        else:
            print("Invalid option")
            return self.admin_menu()

    def generate_attendees(self):
        print("We have the following flight trips available:  ")
        exported_data = pd.read_sql_query('SELECT Flight_ID, Destination FROM Flight_Trip', self.connection)
        df_2 = pd.DataFrame(exported_data)
        print(df_2)
        flight_id = input("What is the flightID?    ")
        query=(f"SELECT Customers.PassportID, Customers.FirstName, Customers.Surname, Customers.Gender, Flight_Trip.Destination, Customers.Boarded_Flight FROM Customers INNER JOIN Flight_Trip ON Customers.Flight_ID=Flight_Trip.Flight_ID WHERE Customers.Flight_ID={flight_id} and Customers.Boarded_Flight=0")
        exported_data = pd.read_sql_query(query,self.connection)
        df_2 = pd.DataFrame(exported_data)
        print(df_2)

        generate_csv = input("Would you like to generate a csv file of the flight attendees? (Y/N)    ")
        if generate_csv.lower() == "y":
            file_path = input("Please enter the location you would like the csv file    ")
            file_name = input("What would you like the file name to be called?    ")
            df_2.to_csv(fr'{file_path}\{file_name}.csv')
        else:
            return self.user_interface()



test = User_functions()
test.login()