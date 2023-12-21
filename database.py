import mysql.connector


class SQL():
    def command(self, com):
        return(self.mycursor.execute(com))
    
    def get_all(self, tablename):
        self.command("SELECT * FROM "+tablename)
        return(self.mycursor.fetchall())

    def connect(self, database_name):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=database_name
        )
        self.mycursor = self.mydb.cursor()

    def create_database(self, database_name):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        self.mycursor = self.mydb.cursor()
        self.command("CREATE DATABASE "+database_name)

    def create_table(self, nameAndData):
        self.command("CREATE TABLE "+nameAndData)

    def __init__(self):
        self.mydb=None
        self.mycursor=None
        try:
            self.create_database("boiler")
            print("Database created")
        except:
            print("Database exists")
        self.connect("boiler")
        try:
            self.create_table("log (time VARCHAR(255), value INT)")
            print("log table created")
        except:
            print("log table exists")
        try:
            self.create_table("rt_temp (active BOOL, userValue INT, meterValue INT)")
            print("rt_temp table created")
        except:
            print("rt_temp table exists") #rt_temp means real time temperature