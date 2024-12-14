import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user, 
            password=self.password,
            database=self.database
        )
        
    def get_customer_by_id(self, customer_id):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customer WHERE customer_id = %s', (customer_id,))
        customer = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return customer
    
    def get_customer_history(self, customer_id):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM history NATURAL JOIN item WHERE customer_id = %s', (customer_id,))
        history = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return history
