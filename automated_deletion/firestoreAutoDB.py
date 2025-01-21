import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

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
    
    def deleteExpired(self):
        print("\n<====================>")
        print("DELETE EXPIRED CSV")
        print("<====================>")
        print("Deleting expired csv from database")
        query = self.db.collection('items').where('expiration_date', '<=', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for doc in query.stream():
            self.db.collection('items').document(doc.id).delete()
            print(f"Deleted item {doc.id}")
        print('CSV deletion complete')
        
