import sys
import os
import io
from flask import Flask, request, jsonify
import ML_model.MachineCustomerItemDataConvertor as mc
import ML_model.ItemDataConvertor as ic
import ML_model.Model as md
import ML_model.firestoreDB as db
from dotenv import load_dotenv
from AI_Agents.Conversable_Agent import main as agent
from emailservice import send_email
import uuid
import AI_Agents.Seach_Agent as SearchAgent
import AI_Agents.Product_Selection_Agent as ProductSelectionAgent
import AI_Agents.Data_Extract_Agent as DataExtractAgent
import AI_Agents.Data_frame_creator_Agent as DataFrameCreatorAgent
from flask_cors import CORS
load_dotenv()

# Example request data
# {
#     "secret_key": "G6QJ6DDNI0C9",
#     "item_name": "Tomato Sauce Bottle", 
#     "custom_domains": ["https://www.amazon.com"],
#     "price_level": 3, 
#     "tags": ["Tomato","Quality"]
# }

app = Flask(__name__)
CORS(app)


@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        print("\n<====================>")
        print("RECOMMENDATION REQUEST")
        print("<====================>")

        # request_id = str(uuid.uuid4())
        request_id = "1234567890"
        
        # Get request data and create machine customer
        print("Getting request data...")
        request_data = request.get_json()
        print(f"Request data received")

        print("Matching with machine customer...")
        try:
            machine_customer = mc.create_machine_customer(request_data)
            mc.print_machine_customer(machine_customer)
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        database1 = db.FirestoreDB()
        state,csv_file = database1.check_csv(request_data['item_name'],machine_customer.country)
        
        print("Check csv data")
        if state:
            print("Found existing CSV file for this item and country...")
        else:
            print(f"Agent workflow started for request {request_id}...")
            # Run the agent - output will only go to file
            agent(request_data["item_name"], 
                  request_data["custom_domains"], 
                  request_data["tags"],
                  machine_customer.country,
                  request_id)

            print("Agent workflow completed...")
            state,csv_file = database1.check_csv(request_data['item_name'],machine_customer.country)
                
        # Get items from CSV and create model
        print("\nLoading items from CSV...")
        # items = ic.csv_to_list(os.path.join("Final_products", csv_filename))
        items = ic.csv_to_list_firebase(csv_file)
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
            database = db.FirestoreDB()
            database.add_search_item(machine_customer.customer_id, result)
            print("Sending email...")
            print(send_email(machine_customer.customer_name, machine_customer.email, result, request_data["item_name"]))
            return jsonify({"status": "success and email sent"})
        except Exception as e:
            print(f"Error during model execution: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/health', methods=['GET']) 
def health(): 
    print("got the request")
    return jsonify({"status": "healthy"}),200

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=8000, threaded=True, use_reloader=False)
