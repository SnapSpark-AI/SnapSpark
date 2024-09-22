import mysql.connector
import os

def create_firedb():
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USR"),
        password=os.getenv("MYSQL_PASS"),
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE firedb")
    mydb.commit()

def create_conditions_table():
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USR"),
        password=os.getenv("MYSQL_PASS"),
        database="firedb"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE TABLE conditions (filename VARCHAR(255), temperature VARCHAR(255), humidity VARCHAR(255), weather_speed VARCHAR(255))")
    mydb.commit()
    
def init_db():
    print("1 - Create firedb")
    print("2 - Create conditions table")
    print("")
    inp = int(input(">>> "))
    if inp == 1:
        create_firedb()
    elif inp == 2:
        create_conditions_table
    
if __name__ == "__main__":
    init_db()