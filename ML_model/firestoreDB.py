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
    
    def add_search_result(self, item_id,item_score,customer_id):
        print(f"\nAdding search result for Item ID: {item_id}, score: {item_score}")
        self.db.collection("customer").document(customer_id).collection("history").add(dict({("timestamp",""),("items",item_id),("score",item_score)}))

    def add_search_item(self,customer_id, item_array):
        print(f"\nAdding search items for Customer ID: {customer_id}")
        item_suggested = []
        item_suggested_score = []
        for item in item_array:
            state,item_id = self.get_item_id(item.link,item.name)
            print(f"Item ID: {item_id}")
            if not state:
                print("Item not found, adding to database")
                doc = self.db.collection("item").add(dict({("name",item.name),("link",item.link),("price",item.price),("description",item.description),("rate",item.rate),("tags",item.tags),("image_link",item.image_link)}))
                item_id = doc.id
            item_suggested.append(item_id)
            item_suggested_score.append(item.score)
        self.add_search_result(item_suggested,item_suggested_score,customer_id)


    def get_users(self):
        """
        Retrieve all users from the database
        
        Returns:
            list: List of all users
        """
        docs = self.db.collection("customer").get()
        return docs

    def get_item_id(self, item_link, item_name):
        query = self.db.collection("item").where("name","==",item_name)
        query = query.where("link","==",item_link)
        query = query.stream()
        if query.count() > 0:
            item = query.get()
            return True,item.id
        else:
            return False,0
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

