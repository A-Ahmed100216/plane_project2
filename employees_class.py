from people_class import People
from db_connection import DB_Connection


class Employees(People):
    def __init__(self, passport_number, first_name, surname, gender, occupation):
        super().__init__(passport_number, first_name, surname)
        self.gender = gender
        self.occupation = occupation
        # connection instance to be used later
        self.test = DB_Connection()

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
            print("Employees table does not exist, please try again")


    # function to show all the employees in records
    def show_all_employees(self):
        if self.test.cursor.tables(table="Employees", tableType="TABLE").fetchone():
            employees = self.test.connection.execute("""SELECT * FROM Employees""").fetchall()
            # for loop to print all thw records in the table
            for rows in employees:
                print(rows)
        else:
            print("Employees table does not exist, please try again")


if __name__ == "__main__":
    employees = Employees("102901092", "Chicken", "Little", "Male", "Pilot")
    employees.add_to_employees_table("102901092", "Chicken", "Little", "Male", "Pilot", "1")