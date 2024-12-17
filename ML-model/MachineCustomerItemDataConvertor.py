import DataTypes as dt
import UserFixedDataConvertor as uc
import Database as db
import bcrypt

# POST MAN request
# {
#     "email": "test@test.com",
#     "password": "test",
#     "item_name": "laptop",
#     "price_level": 1,
#     "tags": ["portable","mac"],
#     "isHistory": True
# }

def create_machine_customer(request):
    database = db.Database("localhost","root","root","machine_customer")

    customer = database.get_customer_by_email(request["email"], request["password"])
    if customer is None:
        raise ValueError("Customer not found")
    mc= dt.MachineCustomer(customer[0], request["item_name"], request["price_level"], request["tags"])
    try:
        if request["isHistory"]:
            mc.isHistory = request["history"]
    except:
        pass
    if mc.isHistory:
        mc.history = fetchHistory(mc.customer_id)
    return mc

def print_machine_customer(machine_customer):
    print(f"Customer ID: {machine_customer.customer_id}")
    print(f"Item Name: {machine_customer.item_name}")
    print(f"Price Level: {machine_customer.price_level}")
    print(f"Tags: {machine_customer.tags}")
    print(f"Is History: {machine_customer.isHistory}")

def fetchHistory(customer_id):
    """Build history list for the customer from database"""
    history = uc.buildHistoryList(customer_id)
    return history


# print_machine_customer(create_machine_customer({"customer_id": 1, "item_name": "laptop", "price_level": 1, "tags": ["portable","mac"], "isHistory": True}))

