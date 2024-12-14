# Import required modules
import Database as db
import DataTypes as dt

# Initialize database connection
database = db.Database("localhost","root","root","machine_customer")

def buildHistoryList(customer_id):
    """Build list of historical items purchased by a customer"""
    print(f"\nFetching purchase history for customer {customer_id}")
    
    # Get customer's purchase history from database
    customer_history = database.get_customer_history(customer_id)
    print(f"Found {len(customer_history)} historical purchases")
    
    history = []
    # Convert each history record into Item object
    for h in customer_history:
        print(f"Processing history record: {h[3]}")
        # Create Item with: name, price, description, link, rating, tags, quantity
        item = dt.Item(h[3], h[4], h[5], h[6], h[7], h[8].lower().split(','),h[2])
        history.append(item)
        print(f"Added {item.name} to history list")
    
    print(f"Returning history list with {len(history)} items")
    return history
