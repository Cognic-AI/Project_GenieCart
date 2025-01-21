import os
import json
import csv
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List
import ML_model.firestoreDB as db
load_dotenv()

# Initialize Gemini with API key cycling
class GeminiKeyManager:
    def __init__(self) -> None:
        self.api_keys: List[str] = [
            os.getenv("GEMINI_API_KEY_1"),
            os.getenv("GEMINI_API_KEY_2"), 
            os.getenv("GEMINI_API_KEY_3"),
            os.getenv("GEMINI_API_KEY_4"),
            os.getenv("GEMINI_API_KEY_5"),
        ]
        if not all(self.api_keys):
            raise ValueError("One or more GEMINI_API_KEYS are missing from environment variables.")
        self.current_index: int = 0

    def get_next_key(self) -> str:
        """Returns the next API key and cycles to the next one."""
        key: str = self.api_keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.api_keys)
        return key

key_manager = GeminiKeyManager()

def initialize_gemini():
    gemini_api_key = key_manager.get_next_key()
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.6,
        "top_k": 10,
        "max_output_tokens": 20,
        "response_mime_type": "application/json",
    }
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

def get_gemini_response(model, prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return None

def filter_json_data(item_name: str, product_name: str, model) -> bool:
    prompt = f"""
    Decide if the following product name somehow matches the item name provided:

    Item name: {item_name}
    Product name: {product_name}

    Respond with "true" if it matches, and "false" if it does not.
    """

    response = get_gemini_response(model, prompt)
    return "true" in response.lower()

def json_to_csv(item_name: str,country_code: str,request_id: str) -> None:

    print("------------------------------------------------------------------------------------------------")
    print("Data frame creator agent started")

    json_folder = os.path.join("Final_products",f"Final_products_{request_id}")
    output_csv = os.path.join("Final_products",f"{item_name}_{country_code}_{request_id}.csv")

    # Ensure the folder exists
    if not os.path.exists(json_folder):
        raise FileNotFoundError(f"The folder {json_folder} does not exist.")

    # Get a list of all JSON files in the folder
    json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
    if not json_files:
        raise ValueError("No JSON files found in the specified folder.")

    # Open the CSV file for writing
    data_to_fire = []
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = None

        for json_file in json_files:
            json_path = os.path.join(json_folder, json_file)

            with open(json_path, mode="r", encoding="utf-8") as f:
                # Load the JSON data
                data = json.load(f)

                # Convert all keys to lowercase
                data = {key.lower(): value for key, value in data.items()}

                # Initialize Gemini
                model = initialize_gemini()

                # Extract only the product_name from the JSON
                product_name = data.get("product_name", "")
                if not filter_json_data(item_name, product_name, model):
                    continue

                price = data.get("price", "")
                if price == "" or price is None:
                    continue
                try:
                    float(price)  # Try converting to float
                except (ValueError, TypeError):
                    continue

                currency = data.get("currency", "")
                if currency == "USD":
                    data["currency"] = "$"

                currency = data.get("currency", "")
                if currency != "$":
                    continue
                
                availability = data.get("availability", "")
                if availability == False:
                    continue

                print("Product requirements matched")

                # Initialize the CSV writer with headers on the first file
                if writer is None:
                    headers = data.keys()
                    writer = csv.DictWriter(csv_file, fieldnames=headers)
                    writer.writeheader()  # Write the header row

                # Write the JSON data as a row in the CSV file
                writer.writerow(data)
                data_to_fire.append(data)
    
    # add to firebase
    database = db.FirestoreDB()
    database.add_csv(data_to_fire,item_name,country_code,request_id)

    print(f"CSV file has been created at {output_csv}")

    print("Data frame creator agent completed")
    print("------------------------------------------------------------------------------------------------")

# Example usage
# json_to_csv("Tomato Ketchup","US","1234567890")
