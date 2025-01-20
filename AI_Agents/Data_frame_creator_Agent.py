import os
import json
import csv
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

def initialize_LLAMA():
    LLAMA_api_key = os.getenv("LLAMA_API_KEY")
    if not LLAMA_api_key:
        raise ValueError("LLAMA is not set in the environment variables.")
    LLAMA_client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=LLAMA_api_key
    )

    return LLAMA_client

def get_LLAMA_response(LLAMA_client: OpenAI, prompt: str) -> str:
    try:
        completion = LLAMA_client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that filters the products based on the item name provided."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            top_p=0.7,
            max_tokens=100
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting LLAMA response: {e}")
        return None

def filter_json_data(item_name: str, product_name: str, LLAMA_client: OpenAI) -> bool:

    prompt = f"""
    Decide if the following product name somehow matches the item name provided:

    Item name: {item_name}
    Product name: {product_name}

    Respond with "true" if it matches, and "false" if it does not.
    """

    response = get_LLAMA_response(LLAMA_client, prompt)
    return "true" in response.lower()

def json_to_csv(item_name: str,country_code: str,request_id: str) -> None:

    print("------------------------------------------------------------------------------------------------")
    print("Data frame creator agent started")

    json_folder = os.path.join("Final_products",f"Final_products_{request_id}")
    output_csv = os.path.join("Final_products",f"{item_name}_{country_code}_{request_id}.csv")

    # Initialize Gemini
    LLAMA_client = initialize_LLAMA()

    # Ensure the folder exists
    if not os.path.exists(json_folder):
        raise FileNotFoundError(f"The folder {json_folder} does not exist.")

    # Get a list of all JSON files in the folder
    json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
    if not json_files:
        raise ValueError("No JSON files found in the specified folder.")

    # Open the CSV file for writing
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = None

        for json_file in json_files:
            json_path = os.path.join(json_folder, json_file)

            with open(json_path, mode="r", encoding="utf-8") as f:
                # Load the JSON data
                data = json.load(f)

                # Convert all keys to lowercase
                data = {key.lower(): value for key, value in data.items()}

                # Extract only the product_name from the JSON
                product_name = data.get("product_name", "")
                if not filter_json_data(item_name, product_name, LLAMA_client):
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

    print(f"CSV file has been created at {output_csv}")

    print("Data frame creator agent completed")
    print("------------------------------------------------------------------------------------------------")

# Example usage
# json_to_csv("A4 bundle")
