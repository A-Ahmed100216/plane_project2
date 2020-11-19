# import Connection from the connection class that D made
from db_connection import DB_Connection

# create a People class. Superclass of Passengers and Staff
class People:
    # initialise the class with variable
    def __init__(self, passport_number, first_name, surname):
        self.passport_number = passport_number
        self.first_name = first_name
        self.surname = surname
        # need to create an instance of the connection class to use
        self.test = DB_Connection()

    # function to create a table within the database for passengers
    def create_customer_table(self):

        if self.test.cursor.tables(table="Customers", tableType="TABLE").fetchone():

            # stop the function and print message if table is already created
            print("Customers table is already created")
        else:
            # create the tables

            print("Creating customers table \n")
            self.test.cursor.execute("""CREATE TABLE Customers(
                                PassportID VARCHAR(20) NOT NULL PRIMARY KEY,
                                TaxNumber VARCHAR(20) NOT NULL,
                                FirstName VARCHAR(MAX) NOT NULL,
                                Surname VARCHAR(MAX) NOT NULL,
                                Flight_ID INT NOT NULL REFERENCES Flight_Trip(Flight_ID),
                                Gender VARCHAR(10),
                                Boarded_Flight BIT
                                );""")
            self.test.cursor.commit()

    # function to create a table within the database for the staff
    def create_employee_table(self):

        if self.test.cursor.tables(table="Employees", tableType="TABLE").fetchone():

            # stop the function and print message if table is already created
            print("Employees table is already created")
        else:

            print("Creating employees table \n")
            self.test.cursor.execute("""CREATE TABLE Employees(
                                    StaffPassportID VARCHAR(20) NOT NULL PRIMARY KEY,
                                    FirstName VARCHAR(MAX) NOT NULL,
                                    Surname VARCHAR(MAX) NOT NULL,
                                    Flight_ID INT NOT NULL REFERENCES Flight_Trip(Flight_ID),
                                    Gender VARCHAR(10),
                                    Occupation VARCHAR(20)
                                    );""")
            self.test.cursor.commit()


# only do these tests if running from this file
if __name__ == "__main__":
    testing = People("1235876910", "Chicken", "Little")
    testing.test
    print(testing.passport_number)
    print(testing.first_name)
    print(testing.surname)
    testing.create_customer_table()
    testing.create_employee_table()