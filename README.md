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

## 1. Connection Class - Donovan 
* This is main parent class from which all others inherit. This class establishes a connection with the database.
* The pyodbc module is imported to allow for a connection to be established. This module was installed into the environment using the following command ```pip install pyodbc```
* The class is initialised with several attributes such as server, database, username, and password. A new database and server was utilised for the purposes of this project, to minimise connection related issues. 
* The process is as follows:
1. Import pyodbc to use method that connects to DB.  
```python
import pyodbc
```

2. Create a class that holds attributes with the details of the DB.
```python
class DB_Connection():
    def __init__(self):
        self.server = "hashimoto.duckdns.org"
        self.database = "bada_airlines"  # the name of our newly created database
        self.username = "**"
        self.password = "*****"
```

3. Establish a connection with the driver
```python
self.connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
```
4. Create a cursor in order to interact with the DB
```python
self.cursor = self.connection.cursor()
```

5. Run some tests in order to see if the connection has been made
```python
if __name__ =="__main__":
    test = DB_Connection()
    test.__init__()
```

## 2. Aircraft Class - Aminah 

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
## 3. People Class - Amaan
* Import the class to enable connection to the database
```python
# import Connection from the connection class that D made
from db_connection_class import DB_Connection
```
* Create a class for People, and initiate it with the tax_number, first_name, and surname variables
```python
# create a People class. Superclass of Passengers and Staff
class People:
    # initialise the class with variable
    def __init__(self, passport_number, first_name, surname):
        self.passport_number = passport_number
        self.first_name = first_name
        self.surname = surname
```
* **Note, the Flight_Trip table must have been created before these functions to create these tables are called, due to them referencing this table**
* Create a function to create the actual table to hold the customers, with a check if the table has already been made (and prints a message if has), otherwise creates the table
```python
# function to create a table within the database for passengers
    def create_customer_table(self):
        if self.cursor.tables(table="Customer", tableType="TABLE").fetchone():
            # stop the function and print message if table is already created
            print("Customers table is already created")
        else:
            # create the tables
            self.cursor.execute("""CREATE TABLE Customer(
                                PassportID VARCHAR(20) NOT NULL IDENTITY PRIMARY KEY,
								TaxNumber VARCHAR(20) NOT NULL,
                                FirstName VARCHAR(MAX) NOT NULL,
                                Surname VARCHAR(MAX) NOT NULL,
                                FlightID INT NOT NULL REFERENCES Flight_Trip(FlightID),
                                Gender VARCHAR(10),
                                Boarded_Flight BOOLEAN
                                );""")
```  
* Create a function to create the Employee table, with the same constraints
```python
# function to create a table within the database for the staff
    def create_employee_table(self):
        if self.cursor.tables(table="Employee", tableType="TABLE").fetchone():
            # stop the function and print message if table is already created
            print("Employee table is already created")
        else:
            self.cursor.execute("""CREATE TABLE Staff(
                                    StaffPassportID VARCHAR(20) NOT NULL IDENTITY PRIMARY KEY,
                                    FirstName VARCHAR(MAX) NOT NULL,
                                    Surname VARCHAR(MAX) NOT NULL,
                                    FlightID INT NOT NULL REFERENCES Flight_Trip(FlightID),
                                    Gender VARCHAR(10),
                                    Occupation VARCHAR(20)
                                    );""")
```  
* Create some tests in an if __name__ == "__main__" statement so that they only run when this file is being called directly.
```python
 # initialise an object for testing
    testing = People("1235876910", "Chicken", "Little")
    # print out various attributes to make sure that it has
    # been properly initialised
    print(testing.passport_number)
    print(testing.first_name)
    print(testing.surname)
    # test the creation of tables functions
    testing.create_customer_table()
    testing.create_employee_table()
```

   

## 4. Admin Class - Aminah 
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


## 5. Flight Trip Class - Donovan 
1. Import the relevant classes and modules
```python
from db_connection_class import DB_Connection
import pandas as pd
from aircraft_class import Aircraft
```
2. Create a class called Flight_Trip. Inherit from the DB_Connection class
```python
class Flight_Trip(DB_Connection):
    def __init__(self):
        super().__init__()
```

3. Create methods in the class too...
   1. Create table
```python
    def create_table(self):
        self.cursor.execute("CREATE TABLE Flight_Trip (Flight_ID INT NOT NULL IDENTITY(1,1) PRIMARY KEY, craft_id INT, Destination VARCHAR(100), Duration_hrs INT, Date VARCHAR(100), Time VARCHAR(100));")
```
   2. View table
```python
    def view_table(self):
        flights_table = self.cursor.execute("SELECT * FROM Flight_Trip").fetchall() # fetches all the info in the table
        return flights_table
```  
   3. Add existing data into the table
```python
 def existing_flights(self):
        self.cursor.execute("INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (1, 'Marbella', 2, '12/12/2019', '12:00');")
        self.cursor.execute("INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (2, 'St Lucia', 8, '14/12/2019', '01:00');")
        self.cursor.execute(
            "INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (4, 'Los Angeles', 10, '14/05/2019', '08:00');")
        self.cursor.execute(
            "INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time) VALUES (3, 'Antigua', 9, '06/06/2019', '10:00');")
        self.connection.commit()
``` 
   4. Enable the user to input data
```python
    def add_flight(self):
        craft_id = input("Please enter the aircraft ID number for this flight ==> ")
        destination = input("Where are you flying to? ==> ")
        duration = int(input("How many hours is this flight? ==> "))
        date = input("Please enter the date of this flight(dd/mm/yyy) ==> ")
        time = input("What time is the flight?(hh:mm) ==> ")
        self.cursor.execute(f"INSERT INTO Flight_Trip (craft_id, Destination, Duration_hrs, Scheduled_Date, Scheduled_Time ) VALUES ('{craft_id}', '{destination}', '{duration}', '{date}','{time}');")
        self.connection.commit()
        print(f"Success. Flight to {destination} added")
```
   5. Enable user to change the plane assigned to a flight trip
```python
    def change_plane(self):
        print("We have the following flight trips available:  ")
        exported_data = pd.read_sql_query('SELECT Flight_ID, Destination FROM Flight_Trip', self.connection)
        df_2 = pd.DataFrame(exported_data)
        print(df_2)
        flight_id=input("Please select the flight id where you wish to assign a new aircraft ==> ")
        new_craft_id=input("Please enter the new craft id you wish to assign ==> ")
        self.cursor.execute(f"UPDATE Flight_Trip SET craft_id={new_craft_id} WHERE Flight_ID={flight_id}")
        self.connection.commit()
```
4. Test your code
```python
if __name__=="__main__":
    test = Flight_Trip()
    test.create_table()
    test.existing_flights()
    test.add_flight()
    print(test.view_table())
```


## 6. Customers Class - Amaan 

* First import the People and DB_Connection classes
```python
from people_class import People
from db_connection import DB_Connection
```
* Create the class Customer that inherits from People
```python
# Class for the Customers that inherits from People
class Customer(People):
```
* Declare the variables in the constructor (.i.e. __init__ method)
```python
# initialise the class
    def __init__(self, passport_number, first_name, surname, tax_number):
        # inherit these variables from the people class
        super().__init__(passport_number, first_name, surname)
        self.tax_number = tax_number
        # connection instance to be used later,
        # rather than inherit from this class
        self.test = DB_Connection()
```  
* A relatively simple function to add a user to the Customers table is seen below. It takes all the attributes within the function call, so that the user can be asked for input within the user_interface file further down the road, which is then piped into this function
```python
# Add data to the Customer table using INSERT
    def add_to_customer_table(self, passport_number, first_name, surname,tax_number, flight_id, gender, boarded_flight):
        # check if the table is created
        if self.test.cursor.tables(table="Customers", tableType="TABLE").fetchone():
            # do the SQL INSERT queries
            self.test.connection.execute(f"""INSERT INTO Customers(
                                        PassportID,TaxNumber,FirstName,Surname,Flight_ID,Gender,Boarded_Flight
                                        ) VALUES (
                                        '{passport_number}','{tax_number}','{first_name}','{surname}',{flight_id},
                                        '{gender}', {boarded_flight});""")
            # commit the SQL statement to the database
            self.test.connection.commit()
        else:
            # a message to inform the user what is going on
            print("Customers table does not exist, please try again")

```  
* A function to show all the current customers utilises a simple SELECT * FROM <table_name> statement with a for loop to output the results
```python
# function to show all the customers
    def show_customers(self):
        # check if the table is created
        if self.test.cursor.tables(table="Customers", tableType="TABLE").fetchone():
            customers = self.test.cursor.execute("""SELECT * FROM Customers""")
            # for loop to print all the rows of customers
            for rows in customers:
                print(rows)
        else:
            # a message to inform the user what is going on
            print("Customers table does not exist, please try again")
```  
* Again, tests are done at the end of the file to ensure things are running smoothly
```python
# used to ensure these tests only are done when calling from this file
if __name__ == "__main__":
    customer = Customer("68546354", "Harry", "Potter", "653214")
    customer.add_to_customer_table("68546354", "Harry", "Potter", "653214", "2", "Male", 0)
```



## 7. Employees Class - Amaan
* Import from the relevant libraries and classes (the same ones as in the Customer class)
```python
# import from the relevant files
from people_class import People
from db_connection import DB_Connection
```
* Create the Employee class that inherits from People
```python
# create the class that inherits from People
class Employees(People):
```
* Initialise the class and the attributes
```python
# initialise the class
    def __init__(self, passport_number, first_name, surname, gender, occupation):
        # inherit these variables from the People class
        super().__init__(passport_number, first_name, surname)
        self.gender = gender
        self.occupation = occupation
        # connection instance to be used later
        self.test = DB_Connection()
```  
* A function to add an employee to the Employee table. Functionally similar to the add_to_customer_table function in Customer
```python
# Add data to the Customer table using INSERT
    def add_to_employees_table(self, passport_number, first_name, surname,
                               gender, occupation, flight_id):
        # check if the table is created
        if self.test.cursor.tables(table="Employees", tableType="TABLE").fetchone():
            # do the SQL INSERT queries
            self.test.connection.execute(f"""INSERT INTO Employees(
                                        StaffPassportID,FirstName,Surname,Flight_ID,Gender,Occupation
                                        ) VALUES (
                                        '{passport_number}','{first_name}','{surname}','{flight_id}',
                                        '{gender}', '{occupation}'
                                      );""")
            self.test.connection.commit()
        else:
            # message to show user if table does not exist
            print("Employees table does not exist, please try again")
```  
* A function to show all employees, again, functionally similar to the customer variant
```python
# function to show all the employees in records
    def show_all_employees(self):
        # check if the table has been created
        if self.test.cursor.tables(table="Employees", tableType="TABLE").fetchone():
            employees = self.test.connection.execute("""SELECT * FROM Employees""").fetchall()
            # for loop to print all thw records in the table
            for rows in employees:
                print(rows)
        else:
            # message to show user if table does not exist
            print("Employees table does not exist, please try again")
```  
* Finally, some tests are made on an instantiated object of this class, again in such a way that they will only work when this file is being called directly
```python
# testing below this so that they are only run when this file is directly being run
if __name__ == "__main__":
    # instantiate an object and test all the functions
    employees = Employees("102901092", "Chicken", "Little", "Male", "Pilot")
    employees.add_to_employees_table("102901092", "Chicken", "Little", "Male", "Pilot", "1")
    employees.show_all_employees()
```


## 8. Booking Class - Ben
* Import classes and modules 
```python
from db_connection import DB_Connection
import pandas as pd
from aircraft_class import Aircraft
```
* Create a class for Booking which will be a child class of DB_Connection. Initialise the class
```python
class Booking(DB_Connection):

    def __init__(self):
        super().__init__()
        self.ticket_price = 100
        self.total_tickets = 0
```
* Define a method for determining the seats available based upon aircraft capacity. This is done by running a SQL join query.
```python
def available_seats(self):
        print("We have the following flight trips available:  ")
        query=(f"SELECT Flight_Trip.destination as Destination, aircraft.Capacity as Seats_Available , aircraft.craft_id, Flight_Trip.flight_id FROM aircraft INNER JOIN Flight_Trip ON aircraft.craft_id=Flight_Trip.craft_id")
        exported_data = pd.read_sql_query(query, self.connection)
        df_2 = pd.DataFrame(exported_data)
        print(df_2)
```
* Define a method for booking 
```python
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
```
* Define a method for determining the seats remaining. Only adult and child seats are subtracted.

```python
 # Seat counter (See how many seats are available. If seat is sold, subtract from seats available before.)
    def seat_counter(self, adult_tickets, child_tickets,seats_available):
        if adult_tickets > 0:
            seats_available -= adult_tickets
        if child_tickets > 0:
            seats_available -= child_tickets
            return f"There are {seats_available} seats remaining on the flight"
```

* Define a method for displaying the order details. 
```python
# Order details method, prints details in formatted way.
    def order_details(self, flight_id, adult_tickets, child_tickets, lap_child_tickets, order_total):
        # Determine the destination from the flight id
        destination=(self.cursor.execute(f"SELECT destination FROM Flight_Trip WHERE flight_id={flight_id}").fetchone())[0]
        # Insert details into Booking_details table 
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
```
* Test the class using instantaition 
```python
test=Booking()
test.booking()
```










