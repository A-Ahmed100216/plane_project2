import pandas as pd
from db_connection import DB_Connection

# Create an aircraft class and initialise
class Aircraft(DB_Connection):
    def __init__(self):
        super().__init__()
        # Attributes of an aircraft include flying, fueling and landing
        self.fly=bool
        self.refuel=bool
        self.land=bool

    # Create methods for creating table
    def create_aircraft_table(self):
        # Create a table in the database to store aircraft data
        crafts = self.cursor.execute("CREATE TABLE aircraft (craft_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,Type VARCHAR(20), Model VARCHAR(100), Capacity INT, Num_Classes INT, Terminal INT);")
        # self.connection.commit()
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



    def show_aircraft_table(self):
        aircraft_table=self.cursor.execute("SELECT * FROM aircraft").fetchall()
        return aircraft_table

    # Define method for adding new data
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
        self.connection.commit()
        print("Success!")


class Query(DB_Connection):

    def sql_query(self):
        query = input("Please enter your sql query    ")
        exported_data = pd.read_sql_query(f'{query}', self.connection)
        df_2 = pd.DataFrame(exported_data)
        print(df_2)


# Instantiate class
# test=Aircraft()
# test.create_aircraft_table()
# test.plane()
# test.helicopter()
# test.add_aircraft_data()
# print(test.show_aircraft_table())


# query=Query()
# query.sql_query()




