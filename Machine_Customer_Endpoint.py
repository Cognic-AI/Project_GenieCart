import sys
import os
import io
from flask import Flask, request, jsonify
import ML_model.MachineCustomerItemDataConvertor as mc
import ML_model.ItemDataConvertor as ic
import ML_model.Model as md
from ML_model.Database import Database as db
from dotenv import load_dotenv
from AI_Agents.Conversable_Agent import main as agent
from emailservice import send_email

load_dotenv()

# Example request data
# {
#     "secret_key": "nos9qkca",
#     "item_name": "A4 bundle", 
#     "custom_domains": ["https://www.amazon.com"],
#     "price_level": 3, 
#     "tags": ["white","photocopy","a4"]
# }

app = Flask(__name__)

@app.route('/api/recommend', methods=['POST'])
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
        original_stdout = sys.stdout  # Save the original stdout

        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                class DualStream(io.TextIOBase):
                    def __init__(self, file, terminal):
                        self.file = file
                        self.terminal = terminal

                    def write(self, data):
                        self.file.write(data)
                        self.terminal.write(data)

                    def flush(self):
                        self.file.flush()
                        self.terminal.flush()

                dual_stream = DualStream(f, original_stdout)
                sys.stdout = dual_stream  # Redirect stdout to dual stream

                # Run the agent and print output to both file and terminal
                agent(request_data["item_name"], request_data["custom_domains"], request_data["tags"])

        finally:
            sys.stdout = original_stdout  # Restore original stdout

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
    
@app.route('/api/health', methods=['GET']) 
def health_check(): 
    return jsonify({"status": "healthy"}),200

if __name__ == '__main__':
    app.run(debug=False, port=8000, threaded=True, use_reloader=False)
