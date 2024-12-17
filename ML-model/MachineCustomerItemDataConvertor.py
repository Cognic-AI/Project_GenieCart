import DataTypes as dt
import UserFixedDataConvertor as uc
import Database as db
from gemini import generate_llm_tags_for_current_tags
import os
from dotenv import load_dotenv

load_dotenv()

def create_machine_customer(request):
    database = db.Database(os.getenv("DB_HOST"),os.getenv("DB_USER"),os.getenv("DB_PASSWORD"),os.getenv("DB_NAME"),os.getenv("DB_PORT"))

    print(database.get_users())

    customer = database.get_customer_by_email(request["email"], request["password"])

    if customer is None:
        raise ValueError("Customer not found")
    
    mc= dt.MachineCustomer(customer[0], request["item_name"], request["price_level"], generate_llm_tags_for_current_tags(request['item_name'],request["tags"]))
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
