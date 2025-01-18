import ML_model.DataTypes as dt
import ML_model.UserFixedDataConvertor as uc
# import ML_model.Database as db
import ML_model.firestoreDB as db
from ML_model.gemini import generate_llm_tags_for_current_tags
import os
from dotenv import load_dotenv

load_dotenv()

def create_machine_customer(request):
    database = db.FirestoreDB()

    print(database.get_users())
    # print(request["secret_key"])

    customer = database.get_customer_by_key(request["secret_key"])

    if customer is None:
        raise ValueError("Customer not found")
    
    mc= dt.MachineCustomer(customer[0], request["item_name"], request["price_level"], generate_llm_tags_for_current_tags(request['item_name'],request["tags"]), customer[1], customer[2], customer[6])
    mc.history = fetchHistory(mc.customer_id)
    
    return mc

def print_machine_customer(machine_customer):
    print(f"Customer ID: {machine_customer.customer_id}")
    print(f"Item Name: {machine_customer.item_name}")
    print(f"Price Level: {machine_customer.price_level}")
    print(f"Tags: {machine_customer.tags}")

def fetchHistory(customer_id):
    """Build history list for the customer from database"""
    history = uc.buildHistoryList(customer_id)
    return history


# print_machine_customer(create_machine_customer({"customer_id": 1, "item_name": "laptop", "price_level": 1, "tags": ["portable","mac"], "isHistory": True}))
