import firebase_admin
from firebase_admin import credentials,firestore

# cred = credentials.Certificate("genie-cart-firebase-service-account.json")
# firebase_admin.initialize_app(cred)

class FirestoreDB:
    def __init__(self):
        print("\n<====================>")
        print("DATABASE INITIALIZATION")
        print("<====================>")
        print(f"Initializing database connection to Firebase")
        cred = credentials.Certificate("genie-cart-firebase-service-account.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        print("Database initialization complete")
    
    def get_customer_by_key(self, key):
        """
        Retrieve customer information using key
        
        Args:
            key (str): Customer's key
            
        Returns:
            tuple: Customer data if found, None otherwise
        """
        print(f"\nFetching customer with key: {key}")
        
        query = self.db.collection("customer").where("generated_key","==",key)
        result = query.get()

        for doc in result:
            return doc.to_dict()
        if not result:
            return None
    
    def get_customer_history(self, customer_id):
        """
        Retrieve suggestion history for a customer
        
        Args:
            customer_id (int): ID of the customer
            
        Returns:
            list: List of top items suggested for the customer
        """
        print(f"\nFetching purchase history for customer ID: {customer_id}")

        items_id = []  # List to store item IDs
        items_docs = []  # List to store fetched item documents

        # Step 1: Query the 'history' subcollection and sort by 'timestamp'
        query = (
            self.db.collection("customer")
            .document(customer_id)
            .collection("history")
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
        )
        history_docs = query.get()

        # Step 2: Process each document in the 'history' subcollection
        for doc in history_docs:
            data = doc.to_dict()
            if "items" in data and isinstance(data["items"], list):
                items_id.extend(data["items"])  # Append item IDs to the list

        # Step 3: Fetch each item document from the 'item' collection
        for item_id in items_id:
            item_doc_ref = self.db.collection("item").document(item_id)
            item_doc = item_doc_ref.get()
            if item_doc.exists:
                items_docs.append(item_doc.to_dict())  # Add the document data to the list

        return items_docs
    
    def add_search_result(self, customer_id, item_array):
        """
        Add a new search result for a customer
        
        Args:
            customer_id (int): ID of the customer
            item_array (list): List of items from search result
            
        Raises:
            ValueError: If customer_id doesn't exist
        """
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
        print(item_array)
        self.add_search_item(search_id, item_array)
        print("Database connection closed")

    def add_search_item(self, search_id, item_array):
        """
        Add items from a search result to the database
        
        Args:
            search_id (int): ID of the search result
            item_array (list): List of items to add
        """
        print(f"\nAdding search items for search ID: {search_id}")
        for item in item_array:
            item_id = self.get_item_id(item.link,item.name)
            print(f"Item ID: {item_id}")
            conn = self.connect()
            cursor = conn.cursor()
            if item_id<0:
                print("Item not found, adding to database")
                cursor.execute('SET autocommit=0')
                cursor.execute('START TRANSACTION')
                cursor.execute('INSERT INTO item (name, price, description, link, rate, tags,image_link) VALUES (%s, %s, %s, %s, %s, %s,%s)', 
                             (item.name, item.price, item.description, item.link, item.rate, ','.join(item.tags),item.image_link))
                item_id = cursor.lastrowid
                cursor.execute('INSERT INTO search_item (search_id, item_id, score) VALUES (%s, %s, %s)',
                             (search_id, item_id, item.score))
                cursor.execute('COMMIT')
                cursor.execute('SET autocommit=1')
                conn.commit()
            else:
                # print("Item found, adding to search item")
                # cursor.execute('INSERT INTO search_item (search_id, item_id, score) VALUES (%s, %s, %s)',
                #              (search_id, item_id, item.score))
                conn.commit()
            cursor.close()
            conn.close()
        print("Database connection closed")

    def get_users(self):
        """
        Retrieve all users from the database
        
        Returns:
            list: List of all users
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customer')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        print("Database connection closed")
        return users

    def get_item_id(self, item_link, item_name):
        """
        Get the ID of an item from the database based on link and name
        
        Args:
            item_link (str): Link of the item
            item_name (str): Name of the item

        Returns:
            int: Item ID if found, None otherwise
        """
        conn = self.connect()
        cursor = conn.cursor()
        id = -1
        try:
            cursor.execute('SELECT item_id FROM item WHERE link = %s AND name = %s', (item_link, item_name))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            print("Database connection closed")
            print(result)
            if len(result)>0:
                id = result[0][0]  # Return just the ID value
        except Exception as e:
            print(f"Error fetching item ID: {e}")
            cursor.close() 
            conn.close()
            print("Database connection closed")
        finally:
            cursor.close()
            conn.close()
            print("Database connection closed")
            return id
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv
    
#     # Load environment variables
#     load_dotenv()
    
#     # Create database instance
#     database = Database(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"), 
#         database=os.getenv("DB_NAME"),
#         port=os.getenv("DB_PORT", 13467)
#     )
    
#     # Test get_item_id with some sample items
#     test_items = [
#         ("Paper A4 White Printer Copier Fax Paper 100 Sheets", "9.99", "http://example.com/paper"),
#         ("Pencil", "1.99", "http://example.com/pencil"),
#         ("80 GSM A4 Paper 500 Sheets Bundle in White Color", "4.99", "https://www.daraz.lk/products/80-gsm-a4-paper-500-sheets-bundle-in-white-color-i196671991.html")
#     ]
    
#     for item_name, price, link in test_items:
#         print(f"\nTesting get_item_id for item: {item_name}")
#         item_id = database.get_item_id(link)
#         if item_id:
#             print(f"Found item ID: {item_id}")
#         else:
#             print(f"No item found with name: {item_name}")

