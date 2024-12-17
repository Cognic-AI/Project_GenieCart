import mysql.connector

class Database:
    def __init__(self, host, user, password, database, port):
        print("\n<====================>")
        print("DATABASE INITIALIZATION")
        print("<====================>")
        print(f"Initializing database connection to {database} at {host}")
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        print("Database initialization complete")
        
    def connect(self):
        print("\nConnecting to database...")
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user, 
                password=self.password,
                database=self.database,
                port=self.port,  # Explicitly specify default MySQL port
                connect_timeout=10000  # Add timeout
            )
            if connection.is_connected():
                print("Database connection established")
                return connection
            else:
                raise Exception("Failed to establish database connection")
        except mysql.connector.Error as err:
            print(f"Failed to connect to database: {err}")
            # Return more specific error messages
            if err.errno == 2003:
                print("Could not connect to MySQL server. Check if server is running.")
            elif err.errno == 1045:
                print("Invalid username or password")
            elif err.errno == 1049:
                print("Database does not exist")
            raise
        except Exception as err:
            print(f"Unexpected error while connecting to database: {err}")
            raise
    def get_customer_by_email(self, email, password):
        print(f"\nFetching customer with email: {email}")
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customer WHERE email = %s AND password = %s', (email, password))
        customer = cursor.fetchone()
        print(f"Customer data retrieved: {customer}")
        
        cursor.close()
        conn.close()
        print("Database connection closed")
        return customer
    
    def get_customer_history(self, customer_id):
        print(f"\nFetching purchase history for customer ID: {customer_id}")
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM item WHERE item_id IN (SELECT item_id FROM history WHERE customer_id = %s)', (customer_id,))
        history = cursor.fetchall()
        print(f"Retrieved {len(history)} historical purchases")
        
        cursor.close()
        conn.close()
        print("Database connection closed")
        return history
    
    def add_search_result(self, customer_id, item_array):
        print(f"\nAdding search result for customer ID: {customer_id}")
        conn = self.connect()
        cursor = conn.cursor()
        # Check if customer exists before inserting
        cursor.execute('SELECT customer_id FROM customer WHERE customer_id = %s', (customer_id,))
        if not cursor.fetchone():
            raise ValueError(f"Customer ID {customer_id} does not exist")
            
        cursor.execute('INSERT INTO search_result (time_stamp, customer_id) VALUES (NOW(), %s)', (customer_id,))
        conn.commit()
        cursor.close()
        conn.close()
        search_id = cursor.lastrowid
        self.add_search_item(search_id, item_array)
        print("Database connection closed")

    def add_search_item(self, search_id, item_array):
        print(f"\nAdding search items for search ID: {search_id}")
        conn = self.connect()
        cursor = conn.cursor()
        for item in item_array:
            cursor.execute('SET autocommit=0')
            cursor.execute('START TRANSACTION')
            cursor.execute('INSERT INTO item (name, price, description, link, rate, tags) VALUES (%s, %s, %s, %s, %s, %s)', 
                         (item.name, item.price, item.description, item.link, item.rate, ','.join(item.tags)))
            item_id = cursor.lastrowid
            cursor.execute('INSERT INTO search_item (search_id, item_id, score) VALUES (%s, %s, %s)',
                         (search_id, item_id, item.score))
            cursor.execute('COMMIT')
            cursor.execute('SET autocommit=1')
        conn.commit()
        cursor.close()
        conn.close()
        print("Database connection closed")

