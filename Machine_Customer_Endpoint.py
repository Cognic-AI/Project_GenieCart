# from flask import Flask, request, jsonify
# import MachineCustomerItemDataConvertor as mc
# import ItemDataConvertor as ic
# import Model as md
# from Database import Database as db
# import os
# from dotenv import load_dotenv

# POST MAN request
# {
#     "email": "test@test.com",
#     "password": "test",
#     "item_name": "laptop",
#     "price_level": 1,
#     "tags": ["portable","mac"],
# }

# load_dotenv()

# app = Flask(__name__)

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     try:
#         print("\n<====================>")
#         print("RECOMMENDATION REQUEST")
#         print("<====================>")
        
#         # Get request data and create machine customer
#         print("Getting request data...")
#         request_data = request.get_json()
#         print(f"Request data received: {request_data}")
        
#         print("Creating machine customer...")
#         try:
#             machine_customer = mc.create_machine_customer(request_data)
#             mc.print_machine_customer(machine_customer)
#         except ValueError as e:
#             return jsonify({"status": "error", "message": str(e)}), 400
        
#         # Get items from CSV and create model
#         print("\nLoading items from CSV...")
#         items = ic.csv_to_list(os.getenv('PRODUCT_CSV',"product.csv"))
#         print(f"Loaded {len(items)} items")
        
#         # Create model with items and machine customer
#         print("\nCreating recommendation model...")
#         model = md.Model(items, machine_customer)
        
#         # Get recommendations
#         print("\nGetting recommendations...")
#         try:
#             result = model.execute()
#             print("Recommendations generated successfully")
#             print("\nSending response to database...")
#             # Initialize database connection
#             database = db(os.getenv("DB_HOST","localhost"),os.getenv("DB_USER","root"),os.getenv("DB_PASSWORD","root"),os.getenv("DB_NAME","machine_customer"))
#             database.add_search_result(machine_customer.customer_id, result)
#             return jsonify({"status": "success"})
#         except Exception as e:
#             print(f"Error during model execution: {str(e)}")
#             return jsonify({"status": "error", "message": str(e)}), 500
            
#     except Exception as e:
#         print(f"\nERROR: {str(e)}")
#         return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000, threaded=True)

# import DataTypes as dt
# import Model
# import MachineCustomerItemDataConvertor as mc
# import ItemDataConvertor as ic
# import Model as md

# # Create machine customers (3 per real customer, with different item interests)
# machine_customers = [
#     # For John Smith
#     dt.MachineCustomer(1, "phone", 1, tags=["premium", "latest"]),
#     dt.MachineCustomer(1, "laptop", 1, tags=["business", "powerful"]),
#     dt.MachineCustomer(5, "car", 1, tags=["luxury", "sports"]),
    
#     # For Mary Johnson
#     dt.MachineCustomer(2, "phone", 2, tags=["mid-range", "value"]),
#     dt.MachineCustomer(1, "laptop", 1, tags=["portable","mac"],isHistory=True),
#     dt.MachineCustomer(7, "car", 2, tags=["family", "efficient"]),
    
#     # For Bob Wilson
#     dt.MachineCustomer(3, "phone", 3, tags=["budget", "basic"]),
#     dt.MachineCustomer(3, "laptop", 3, tags=["entry-level", "student"]),
#     dt.MachineCustomer(4, "car", 3, tags=["economy", "compact"]),
    
#     # For Alice Brown
#     dt.MachineCustomer(5, "phone", 1, tags=["flagship", "camera"]),
#     dt.MachineCustomer(6, "laptop", 1, tags=["premium", "creator"]),
#     dt.MachineCustomer(6, "car", 1, tags=["premium", "electric"]),
    
#     # For James Davis
#     dt.MachineCustomer(8, "phone", 2, tags=["balanced", "durable"]),
#     dt.MachineCustomer(9, "laptop", 2, tags=["multimedia", "versatile"]),
#     dt.MachineCustomer(10, "car", 2, tags=["midsize", "reliable"])
# ]

# # Create dtems lists
# phones = [
#     dt.Item("iPhone 14 Pro", 999, "Latest Apple flagship", "link1", 4.8, ["premium", "latest", "flagship", "iphone", "pro", "apple"]),
#     dt.Item("Samsung S23 Ultra", 1199, "Premium Android flagship", "link2", 4.9, ["premium", "latest", "samsung", "ultra", "s23"]),
#     dt.Item("Google Pixel 7", 599, "Great camera phone", "link3", 4.7, ["mid-range", "camera", "google", "pixel"]),
#     dt.Item("OnePlus 11", 699, "Fast performance", "link4", 4.6, ["mid-range", "fast", "oneplus"]),
#     dt.Item("iPhone 13", 699, "Previous gen flagship", "link5", 4.7, ["premium", "iphone", "apple"]),
#     dt.Item("Samsung A53", 449, "Mid-range Samsung", "link6", 4.5, ["mid-range", "balanced", "samsung", "a53"]),
#     dt.Item("Motorola G Power", 249, "Budget battery king", "link7", 4.3, ["budget", "battery", "motorola", "power"]),
#     dt.Item("iPhone SE", 429, "Budget iPhone", "link8", 4.4, ["budget", "compact", "iphone", "se", "apple"]),
#     dt.Item("Xiaomi 13", 899, "Premium features", "link9", 4.6, ["premium", "value", "xiaomi"]),
#     dt.Item("Nothing Phone", 749, "Unique design", "link10", 4.5, ["mid-range", "unique", "nothing"]),
#     dt.Item("Sony Xperia 1", 1299, "Premium multimedia", "link11", 4.7, ["premium", "multimedia", "sony", "xperia"]),
#     dt.Item("ASUS ROG Phone", 999, "Gaming focused", "link12", 4.8, ["premium", "gaming", "asus", "rog"]),
#     dt.Item("Samsung Z Fold4", 1799, "Foldable flagship", "link13", 4.7, ["premium", "innovative", "samsung", "fold", "z"]),
#     dt.Item("Google Pixel 6a", 349, "Mid-range Google", "link14", 4.5, ["budget", "camera", "google", "pixel"]),
#     dt.Item("Huawei P50", 899, "Premium build", "link15", 4.6, ["premium", "design", "huawei", "p50"]),
#     dt.Item("Oppo Find X", 949, "Premium features", "link16", 4.7, ["premium", "camera", "oppo", "find", "x"]),
#     dt.Item("Vivo X90", 799, "Premium mid-range", "link17", 4.6, ["mid-range", "camera", "vivo", "x90"]),
#     dt.Item("Nokia X30", 499, "Mid-range durabildty", "link18", 4.4, ["mid-range", "durable", "nokia", "x30"]),
#     dt.Item("Realme GT", 599, "Performance focused", "link19", 4.5, ["mid-range", "fast", "realme", "gt"]),
#     dt.Item("Poco F4", 399, "Budget flagship", "link20", 4.4, ["budget", "performance", "poco", "f4"])
# ]

# laptops = [
#     dt.Item("MacBook Pro 16", 2499, "Premium Apple laptop", "link21", 4.9, ["premium", "powerful", "mac", "pro", "apple"]),
#     dt.Item("Dell XPS 15", 2299, "Premium Windows laptop", "link22", 4.8, ["premium", "business", "dell", "xps"]),
#     dt.Item("Lenovo ThinkPad X1", 1999, "Business laptop", "link23", 4.8, ["business", "reliable", "lenovo", "thinkpad", "x1"]),
#     dt.Item("HP Spectre x360", 1699, "Premium convertible", "link24", 4.7, ["premium", "versatile", "hp", "spectre", "x360"]),
#     dt.Item("ASUS ROG Zephyrus", 2199, "Gaming laptop", "link25", 4.8, ["premium", "gaming", "asus", "rog", "zephyrus"]),
#     dt.Item("Acer Swift 5", 1099, "Ultraportable", "link26", 4.6, ["mid-range", "portable", "acer", "swift"]),
#     dt.Item("Microsoft Surface Laptop", 999, "Clean design", "link27", 4.7, ["mid-range", "design", "microsoft", "surface"]),
#     dt.Item("Dell Inspiron 15", 799, "General purpose", "link28", 4.5, ["mid-range", "general", "dell", "inspiron"]),
#     dt.Item("HP Envy 13", 899, "Premium build", "link29", 4.6, ["mid-range", "premium", "hp", "envy"]),
#     dt.Item("Lenovo Yoga 7i", 899, "Convertible", "link30", 4.6, ["mid-range", "versatile", "lenovo", "yoga"]),
#     dt.Item("ASUS VivoBook", 649, "Budget friendly", "link31", 4.4, ["budget", "value", "asus", "vivobook"]),
#     dt.Item("Acer Aspire 5", 599, "Budget performance", "link32", 4.3, ["budget", "performance", "acer", "aspire"]),
#     dt.Item("HP Pavilion", 699, "Entry level", "link33", 4.4, ["budget", "general", "hp", "pavilion"]),
#     dt.Item("HP Pavilion2", 799, "Entry level", "link33", 4.3, ["budget", "general", "hp", "pavilion"]),
#     dt.Item("Lenovo IdeaPad 3", 549, "Student laptop", "link34", 4.3, ["budget", "student", "lenovo", "ideapad"]),
#     dt.Item("MSI Modern 14", 799, "Slim design", "link35", 4.5, ["mid-range", "portable", "msi", "modern"]),
#     dt.Item("Razer Blade 15", 1999, "Premium gaming", "link36", 4.8, ["premium", "gaming", "razer", "blade"]),
#     dt.Item("LG Gram 17", 1599, "Lightweight premium", "link37", 4.7, ["premium", "portable", "lg", "gram"]),
#     dt.Item("Gigabyte Aero", 1799, "Creator laptop", "link38", 4.7, ["premium", "creator", "gigabyte", "aero"]),
#     dt.Item("Framework Laptop", 999, "Modular design", "link39", 4.6, ["mid-range", "innovative", "framework"]),
#     dt.Item("Chromebook Pixel", 649, "Premium Chromebook", "link40", 4.5, ["budget", "portable", "chromebook", "pixel", "google"])
# ]

# cars = [
#     dt.Item("Tesla Model S", 89990, "Premium electric sedan", "link41", 4.8, ["premium", "electric", "tesla", "model", "s"]),
#     dt.Item("BMW 7 Series", 93400, "Luxury sedan", "link42", 4.9, ["luxury", "premium", "bmw", "7series"]),
#     dt.Item("Mercedes S-Class", 94250, "Ultimate luxury", "link43", 4.9, ["luxury", "premium", "mercedes", "sclass"]),
#     dt.Item("Porsche 911", 106100, "Sports car", "link44", 4.9, ["luxury", "sports", "porsche", "911"]),
#     dt.Item("Audi A8", 86500, "Luxury sedan", "link45", 4.8, ["luxury", "premium", "audi", "a8"]),
#     dt.Item("Toyota Camry", 25945, "Mid-size sedan", "link46", 4.7, ["midsize", "reliable", "toyota", "camry"]),
#     dt.Item("Honda Accord", 26520, "Family sedan", "link47", 4.7, ["family", "reliable", "honda", "accord"]),
#     dt.Item("BMW 3 Series", 43300, "Entry luxury", "link48", 4.7, ["premium", "sports", "bmw", "3series"]),
#     dt.Item("Tesla Model 3", 46990, "Electric sedan", "link49", 4.8, ["premium", "electric", "tesla", "model", "3"]),
#     dt.Item("Hyundai Sonata", 24950, "Mid-size value", "link50", 4.6, ["midsize", "value", "hyundai", "sonata"]),
#     dt.Item("Toyota Corolla", 20425, "Compact car", "link51", 4.6, ["economy", "reliable", "toyota", "corolla"]),
#     dt.Item("Honda Civic", 22550, "Compact car", "link52", 4.7, ["economy", "efficient", "honda", "civic"]),
#     dt.Item("Mazda 3", 21445, "Compact premium", "link53", 4.6, ["economy", "premium", "mazda", "3"]),
#     dt.Item("Volkswagen Golf", 23195, "Compact hatch", "link54", 4.5, ["economy", "practical", "volkswagen", "golf"]),
#     dt.Item("Hyundai Elantra", 20500, "Compact value", "link55", 4.5, ["economy", "value", "hyundai", "elantra"]),
#     dt.Item("Ford Mustang", 27470, "Sports car", "link56", 4.7, ["sports", "performance", "ford", "mustang"]),
#     dt.Item("Chevrolet Corvette", 64995, "Premium sports", "link57", 4.8, ["premium", "sports", "chevrolet", "corvette"]),
#     dt.Item("Lexus ES", 41875, "Entry luxury", "link58", 4.7, ["premium", "comfort", "lexus", "es"]),
#     dt.Item("Audi A4", 39900, "Entry luxury", "link59", 4.7, ["premium", "balanced", "audi", "a4"]),
#     dt.Item("Genesis G70", 37775, "Entry luxury", "link60", 4.6, ["premium", "value", "genesis", "g70"])
# ]

from flask import Flask, request, jsonify
import ML_model.MachineCustomerItemDataConvertor as mc
import ML_model.ItemDataConvertor as ic
import ML_model.Model as md
from ML_model.Database import Database as db
import os
from dotenv import load_dotenv
from AI_Agents.Conversable_Agent import main as agent

load_dotenv()

# {
#     "generated_key": "1234567890",
#     "item_name": "A4 bundle", 
#     "custom_domains": ["https://www.amazon.com", "https://daraz.lk"],
#     "price_level": 3, 
#     "tags": ["white","80gsm","photocopy","a4","100 sheets"]
# }

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        print("\n<====================>")
        print("RECOMMENDATION REQUEST")
        print("<====================>")
        
        # Get request data and create machine customer
        print("Getting request data...")
        request_data = request.get_json()
        print(f"Request data received: {request_data}")

        print("Generating search results...")
        result = agent(request_data["item_name"], request_data["custom_domains"])

        output_filename: str = os.path.join("Agent_Outputs", "Agent_workflow_output.txt")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"Agent workflow output saved to: {output_filename}") 

        print("Matching with machine customer...")
        try:
            machine_customer = mc.create_machine_customer(request_data)
            mc.print_machine_customer(machine_customer)
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        
        # Get items from CSV and create model
        print("\nLoading items from CSV...")
        items = ic.csv_to_list('product.csv')
        print(f"Loaded {len(items)} items")
        
        # Create model with items and machine customer
        print("\nCreating recommendation model...")
        model = md.Model(items, machine_customer)
        
        # Get recommendations
        print("\nGetting recommendations...")
        try:
            result = model.execute()
            print("Recommendations generated successfully")
            print("\nSending response to database...")
            # Initialize database connection
            database = db(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"), 
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                port=os.getenv("DB_PORT",13467)
            )
            database.add_search_result(machine_customer.customer_id, result)
            return jsonify({"status": "success"})
        except Exception as e:
            print(f"Error during model execution: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)

# def recommend():
#     print("\n<====================>")
#     print("RECOMMENDATION REQUEST")
#     print("<====================>")
    
#     print("Creating machine customer...")
#     machine_customer = machine_customers[0]
#     mc.print_machine_customer(machine_customer)
    
#     # Get items from CSV and create model
#     print("\nLoading items from CSV...")
#     items = ic.csv_to_list('product.csv')
#     print(f"Loaded {len(items)} items")
    
#     print("\nCreating recommendation model...")
#     model = md.Model(items, machine_customer)
    
#     # Get recommendations
#     print("\nGetting recommendations...")
#     result = model.execute()
#     print("Recommendations generated successfully")
#     return result

# result = recommend()
# print(result)

