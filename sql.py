import mysql.connector

mydb = mysql.connector.connect(
 host = "127.0.0.1",
 user = "root",
 password = "",
 database = "ciel2025",
)

cursor = mydb.cursor()
request = "SELECT *FROM etudiant"
cursor.execute(request)
result = cursor.fetchall()

for record in result:
    print(record)