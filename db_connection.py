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