import firebase_admin
import pandas as pd
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

class FirestoreDB:
    def __init__(self):
        print("\n<====================>")
        print("DATABASE INITIALIZATION")
        print("<====================>")
        print("Initializing database connection to Firebase")
        if not firebase_admin._apps:
            cred = credentials.Certificate("genie-cart-firebase-service-account.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        print("Database initialization complete")
    
    def get_customer_by_key(self, key):
        print(f"\nFetching customer with key: {key}")
        query = self.db.collection("customer").where("generated_key", "==", key).stream()

        for doc in query:
            return doc.to_dict()
        return None
    
    def get_customer_history(self, customer_id):
        print(f"\nFetching purchase history for customer ID: {customer_id}")
        items_id = []  # List to store item IDs
        items_docs = []  # List to store fetched item documents

        # Step 1: Query the 'history' subcollection and sort by 'timestamp'
        history_docs = (
            self.db.collection("customer")
            .document(customer_id)
            .collection("history")
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .stream()
        )

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
    
    def add_search_result(self, item_id, item_score, customer_id,item_name):
        print(f"\nAdding search result for Item ID(s): {item_id}, score(s): {item_score}")
        self.db.collection("customer").document(customer_id).collection("history").add({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": item_id,
            "score": item_score,
            "item_name":item_name
        })

    def add_purchase(self, item_id, customer_id):
        print(f"\nAdding purchase: {item_id}")
        self.db.collection("customer").document(customer_id).collection("purchase").add({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "item": item_id,
        })

    def add_csv(self, csv_data, item_name,country_code,request_id):
        print(f"\nAdding csv file")
        self.db.collection("csv").document(request_id).set({'item_name':item_name,'country_code':country_code,'expiration_date':
                                                            (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')})
        for i in range(len(csv_data)):
            self.db.collection("csv").document(request_id).collection("data").document(str(i)).set(csv_data[i])
    
    def check_csv(self, item_name, country_code):
        print(f"\nChecking csv file")
        query = self.db.collection("csv").where("item_name", "==", item_name).where("country_code", "==", country_code).stream()
        
        for doc in query:
            docs_ref = self.db.collection("csv").document(doc.id).collection("data").stream()
            csv_data = [doc.to_dict() for doc in docs_ref]
            # print(csv_data)
            # Convert to DataFrame
            
            csv_file = pd.DataFrame(csv_data)
            return True,csv_file
        
        return False,None

    def add_search_item(self, customer_id, item_array,item_name):
        print(f"\nAdding search items for Customer ID: {customer_id}")
        item_suggested = []
        item_suggested_score = []

        for item in item_array:
            state, item_id = self.get_item_id(item.link, item.name)
            if not state:
                print("Item not in the database, adding to database")
                doc_ref = self.db.collection("item").add({
                    "name": item.name,
                    "link": item.link,
                    "price": item.price,
                    "description": item.description,
                    "rate": item.rate,
                    "tags": item.tags,
                    "image_link": item.image_link,
                })
                item_id = doc_ref[1].id
            else:
                print("Item already exists in the database, updating the existing document")
                # If item exists, update the existing document
                self.db.collection("item").document(item_id).set({
                    "name": item.name,
                    "link": item.link, 
                    "price": item.price,
                    "description": item.description,
                    "rate": item.rate,
                    "tags": item.tags,
                    "image_link": item.image_link,
                })
            item_suggested.append(item_id)
            item_suggested_score.append(item.score)

        self.add_search_result(item_suggested, item_suggested_score, customer_id,item_name)
        self.add_purchase(item_id,customer_id)


    def get_users(self):
        """
        Retrieve all users from the database
        
        Returns:
            list: List of all user documents
        """
        docs = self.db.collection("customer").stream()
        return [doc.to_dict() for doc in docs]

    def get_item_id(self, item_link, item_name):
        query = (
            self.db.collection("item")
            .where("name", "==", item_name)
            .where("link", "==", item_link)
            .stream()
        )
        for item in query:
            return True, item.id
        return False, None
