# Engineering74 DevOps - Plane Project 
**Group 1- Amaan, Aminah, Ben, Donovan**

## Task
Create a airline booking system, utilising the following user stories as a guide. 
1. As an airport assistant, I want to be able to create a passenger with name AND passport number so I can add them to the flight.
2. As an airport assistant, I want to be able to create flight_trip with a specific destination. 
3. As an airport assistant, I want to be able to assign and/or change a plane to my flight_trip, input my password so I can handle the problem.
4. As an airport assistant, I want to be able to add passengers to flight_trip so that I can sell tickets to them.
5. As an airport assistant, I want to be able to generate a flight_attendees list with passenger names and passport numbers so I can check their identity. 

## Acceptance Criteria
* Meets user stories
* Utilises OOP

## Planning
For this project, the agile methodology was adopted. This entailed utilising the scrum framework via a tool called Trello which allowed the creation of scrum artifacts such as a product backlog, spring backlog, and increment. The role of Scrum Master was rotated to allow all team members an opportunity to take on this role and take control of the scrum board. While one team member took on the role of scrum master, the remaining members were assigned one of the three amigos, business, testing, development. The roles were also rotated daily to give all team members the opportunity to explore different roles. Three main tasks, or epic stories were identified for this project:
1. Class creation
2. Database creation
3. User Interface creation 
The first stage was to determine the tables required and the relationship between these. This was aided through the creation of an entity relationship diagram. By identifying relationships, it was possible to determine dependencies and prioritise the creation of certain tables prior to others. Following this, these tables could be assigned to classes and any other classes could be identified and subsequently created. The following documentation shall detail the classes created and the process involved.  

## 1. Connection Class
* This is main parent class from which all others inherit. This class establishes a connection with the database.
* The pyodbc module is imported to allow for a connection to be established. This module was installed into the environment using the following command ```pip install pyodbc```
* The class is initialised with several attributes such as server, database, username, and password. A new database and server was utilised for the purpose s of this project, to minimise connection related issues.  

```python
import pyodbc
class DB_Connection:
    def __init__(self):
        self.server = "hashimoto.duckdns.org"
        self.database = "bada_airlines"  # the name of our newly created database
        self.username = "SA"
        self.password = "Passw0rd2020"
        # establish connection
        self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        self.cursor = self.connection.cursor()
```


## 2. Aircraft Class

*  The aircraft class will be a child of the Connection class therefore enabling it to connect to the database. 
* The aircraft class will be used to define methods for inserting and adding data pertaining to aircraft:
    * type - is a plane or helicopter?
    * model - the type of plane or helicopter i.e A380, B777 etc.
    * capacity - what is the capacity of the aircraft
    * number of classes - this refers to the class configuration i.e. first/business/economy or economy/business.
    * terminal - the terminal the craft is located at.
* The class is initialised with aircraft attributes such as fly, refuel and land. These are set to booleans and will be defined in child classes.
* Following ths, methods are established to create a table in the "bada_airlines" database, insert data, view the data in the table, and add new data.

 ```python
# Import relevant modules 
import pandas as pd

# Create an aircraft class and initialise
class Aircraft(DB_Connection):
    def __init__(self):
        super().__init__()
        self.fly=bool
        self.refuel=bool
        self.land=bool


    # Create methods for creating table
    def create_table(self):
        # Create a table in the database to store aircraft data
        crafts = self.cursor.execute("CREATE TABLE aircraft (craft_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,Type VARCHAR(20), Model VARCHAR(100), Capacity INT, Num_Classes INT, Terminal INT);")
        # Commit changes to database
        self.connection.commit()
        return crafts


    # Create plane method for inserting plane data
    def plane(self):
        self.cursor.execute(
            "INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('plane', 'A380',517,3,1)")
        self.cursor.execute(
            "INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('plane', 'B777',364,3,1)")
        self.cursor.execute(
            "INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('plane', 'A320neo',160,2,2)")
        self.cursor.execute(
            "INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('plane', '787 Dreamliner',254,2,1)")
        self.cursor.execute(
            "INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('plane', 'A319',110,2,2)")
        self.connection.commit()


    # Create helicopter method for inserting helicopter data
    def helicopter(self):
        self.cursor.execute(
            "INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('helicopter', 'AS350 B2',5,0,3)")
        self.connection.commit()

    # Method for viewing the data in the table
    def show_table(self):
        aircraft_table=self.cursor.execute("SELECT * FROM aircraft").fetchall()
        return aircraft_table
```
* A method is defined to add new data. While statements have been utilised to prevent invalid data from being inputted.
```python
 def add_aircraft_data(self):
        # Use a while loop to ensure the user enters either helicopter or plane.
        while True:
            craft_type = input("Please enter the type of craft i.e helicopter or plane: ")
            if craft_type=="plane" or craft_type=="helicopter":
                break
            else:
                print("Invalid input")
        # Ask user to input the aircraft model.
        model = input("Please enter the aircraft model: ")
        # Use another while loop to ensure the capacity is a number and realistic
        while True:
            capacity = input("Please enter the craft capacity: ")
            if capacity.isdigit() and 0<int(capacity)<850:
                break
            else:
                print("Invalid input, you have exceeded capacity constraints.")

        while True:
            try:
                travel_class = int(input("Please enter the class configuration: "))
                if 0<=travel_class<=3:
                    break
                else:
                    print("Invalid input, there are a maximum of three classes ")
            except TypeError as err:
                print("Invalid input, please enter a number")

        # Use if statements to assign to terminals automatically
        if craft_type=="plane" and int(capacity)>=200:
            terminal =1
        elif craft_type=="helicopter":
            terminal =3
        else:
            terminal = 2

        self.cursor.execute(f"INSERT INTO aircraft (Type, Model, Capacity, Num_Classes,Terminal) VALUES ('{craft_type}','{model}',{capacity},{travel_class},{terminal})")
        # self.connection.commit()
```

* In order to test the class, it is then instantiated 
```python
# Instantiate class
test=Aircraft()
# test.create_table()
# test.plane()
# test.helicopter()
test.add_data()
print(test.show_table())
```
## 3. People Class

## 4. Admin Class
* The Admin Class is a child of the connection class.
* This class allows the user to carry out administrative actions such as create user logins, add new staff, and add new aircraft. 
* The first stage is to import relevant modules, notably the hashlib package which allows for data to be encrypted. 
* Following this, the Admin class can be created and methods defined. The create user method allows users to create a username and login. The login is then encrypted and stored in the database in an admin table. 
* The add_new_staff and add_new_aircraft methods call functions from imported classes. 
* The class is tested by simply instantiated and testing whether the methods execute as expected. 

```python
from db_connection import DB_Connection
import hashlib
from employees_class import Employees
from aircraft_class import Aircraft

class Admin(DB_Connection):

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

test=Admin()
test.create_user_login()
```


## 5. Flight Trip Class

## 6. Customers Class

## 7. Employees Class

## 8. Booking Class










