from db_connection import DB_Connection
import hashlib
from employees_class import Employees
from aircraft_class import Aircraft

class Admin(DB_Connection):
    # def __init__(self):



    def create_user_login(self):
        firstname=input("Please enter your first name: ")
        lastname=input("Please enter your last name: ")
        username=input("Please enter a username: ")
        password=input("Please enter a password: ")
        result = hashlib.md5(password.encode()).hexdigest()
        self.cursor.execute(f"INSERT INTO admin(First_Name,Last_Name,Username,Password) VALUES('{firstname}','{lastname}','{username}','{result}')")
        self.connection.commit()

    def add_new_staff(self):
        employee=Employees
        employee.add_to_employees_table()

    def add_new_aircraft(self):
        crafts=Aircraft()
        crafts.add_aircraft_data()






# test=Admin()
# test.create_user_login()