# Import relevant modules and classes
from db_connection import DB_Connection
import hashlib
from employees_class import Employees
from aircraft_class import Aircraft

# Admin is a child of DB_Connection
class Admin(DB_Connection):

    # Create user login method
    def create_user_login(self):
        # Ask user for name, username and password
        firstname=input("Please enter your first name: ")
        lastname=input("Please enter your last name: ")
        username=input("Please enter a username: ")
        password=input("Please enter a password: ")
        # Encrpt the password
        result = hashlib.md5(password.encode()).hexdigest()
        # Store encrypted password in database
        self.cursor.execute(f"INSERT INTO admin(First_Name,Last_Name,Username,Password) VALUES('{firstname}','{lastname}','{username}','{result}')")
        self.connection.commit()

    # Define method for adding new staff
    def add_new_staff(self):
        # Create instance of Employees class
        employee=Employees
        # Execute method within Employees class
        employee.add_to_employees_table()

    # Define method for adding new aircraft
    def add_new_aircraft(self):
        # Create instance of Aircraft class
        crafts=Aircraft()
        # Execute method within Aircraft class
        crafts.add_aircraft_data()


# Instantiate to test functionality
# test=Admin()
# test.create_user_login()