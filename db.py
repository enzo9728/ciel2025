import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def connect(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )
        return mydb

    def readAll(self):
        conn = self.connect()
        cursor = conn.cursor()
        req = "SELECT * FROM etudiant"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def readOne(self,id):
        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchone()
        conn.close()
        return data

    def authorized(self, request):
        auth = request.authorization
        username = auth.username
        password = auth.password

        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT password FROM user WHERE login = '{username}'"
        #print(req)
        cursor.execute(req)
        data = cursor.fetchone()
        conn.close()
        if data and (data[0] == password):
            return True
        else:
            return False