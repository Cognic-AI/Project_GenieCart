# Import required modules
# import ML_model.Database as db
import ML_model.firestoreDB as db
import ML_model.DataTypes as dt
import os
import dotenv

dotenv.load_dotenv()

# Initialize database connection
database = db.FirestoreDB()

def buildHistoryList(customer_id):
    """Build list of historical items purchased by a customer"""
    print(f"\nFetching purchase history for customer {customer_id}")
    
    # Get customer's purchase history from database
    customer_history = database.get_customer_history(customer_id)
    print(f"Found {len(customer_history)} historical purchases")
    
    history = []
    # Convert each history record into Item object
    for h in customer_history:
        # print(f"Processing history record: {h}")
        # Create Item with: name, price, description, link, rating, tags, quantity
        item = dt.Item(h['name'], h['price'], h['description'], h['link'], h['rate'], h['tags'])
        history.append(item)
        print(f"Added {item.name} to history list")
    
    print(f"Returning history list with {len(history)} items")
    return history