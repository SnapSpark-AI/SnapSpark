import mysql.connector
import os



mydb = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USR"),
    password=os.getenv("MYSQL_PASS"),
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE firedb")

mydb = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USR"),
    password=os.getenv("MYSQL_PASS"),
    database="firedb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE conditions (filename VARCHAR(255), temperature VARCHAR(255), humidity VARCHAR(255), weather_speed VARCHAR(255))")