from AI_Agents.Conversable_Agent import main as agent
from flask_cors import CORS
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/api/agent', methods=['POST'])
def recommend():
    try:
        request_data = request.get_json()
        agent(request_data["item_name"], 
                  request_data["custom_domains"], 
                  request_data["tags"],
                  request_data["country"],
                  request_data["id"])
        return jsonify({"status": "Agent works are done"})         
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500