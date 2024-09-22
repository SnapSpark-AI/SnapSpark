import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USR"),
    password=os.getenv("MYSQL_PASS"),
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE coordinates (filename VARCHAR(255), latitude VARCHAR(255), longitude VARCHAR(255))")