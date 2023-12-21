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