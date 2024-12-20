import sys
from flask import Flask, request, jsonify
import ML_model.MachineCustomerItemDataConvertor as mc
import ML_model.ItemDataConvertor as ic
import ML_model.Model as md
from ML_model.Database import Database as db
import os
from dotenv import load_dotenv
from AI_Agents.Conversable_Agent import main as agent
from emailservice import send_email

load_dotenv()

# {
#     "secret_key": "nos9qkca",
#     "item_name": "A4 bundle", 
#     "custom_domains": ["https://www.amazon.com"],
#     "price_level": 3, 
#     "tags": ["white","photocopy","a4"]
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
        print(f"Request data received")

        print("Agent workflow started...")

        output_filename: str = os.path.join("Agent_Outputs", "Agent_workflow_output.txt")        
        agent(request_data["item_name"], request_data["custom_domains"], request_data["tags"])
        with open(output_filename, "w") as f:
            sys.stdout = f

        print("Agent workflow completed...")

        print("Matching with machine customer...")
        try:
            machine_customer = mc.create_machine_customer(request_data)
            mc.print_machine_customer(machine_customer)
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        
        # Get items from CSV and create model
        print("\nLoading items from CSV...")
        items = ic.csv_to_list('products.csv')
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
                port=os.getenv("DB_PORT")
            )
            database.add_search_result(machine_customer.customer_id, result)
            print("Sending email...")
            print(send_email(machine_customer.customer_name, machine_customer.email, result, request_data["item_name"]))
            return jsonify({"status": "success and email sent"})
        except Exception as e:
            print(f"Error during model execution: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=True, use_reloader=False)
