import mysql.connector


class SQL():
    def command(self, com):
        self.mycursor.execute(com)
    
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

    def create_rt_temp_record(self):
        cmd="INSERT INTO rt_temp (active, userValue, meterValue) VALUES ("+str(self.active)+", "+str(self.userValue)+", "+str(self.meterValue)+")"
        self.command(cmd)

    def set_user(self, val):
        self.userValue=val
    def set_meter(self, val):
        self.meterValue=val
    def set_active(self, val):
        self.active=val
    def get_user(self):
        return self.userValue
    def get_meter(self):
        return self.meterValue
    def get_active(self):
        return self.active

    def __init__(self):
        self.mydb=None
        self.mycursor=None
        self.userValue=0
        self.meterValue=0
        self.active=0