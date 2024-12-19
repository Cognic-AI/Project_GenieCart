import os
import pandas as pd
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_llm_tags_single(name,description):
    """Use an LLM to generate relevant tags for an item based on its name and description"""
    print(f"\nGenerating LLM tags for item: {name}")
    import google.generativeai as genai
    
    # Configure the Gemini API
    print("Configuring Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return []
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    print("Generating prompt...")
    prompt = f"""Generate relevant product tags for the following item:
    Name: {name}
    Description: {description}
    
    Return only a comma-separated list of relevant single-word tags in lowercase, with no explanations.
    Focus on product categories, features, use cases, and key attributes."""

    try:
        print("Generating tags using LLM...")
        response = model.generate_content(prompt)
        
        # Extract tags from response and clean them
        print("Processing LLM response...")
        llm_tags = response.text.strip().split(',')
        llm_tags = [tag.strip().lower() for tag in llm_tags]
        
        print(f"Generated {len(llm_tags)} tags: {llm_tags}")
        return llm_tags
    except Exception as e:
        print(f"Error generating LLM tags: {e}")
        return []
    
def generate_llm_tags_bulk(df):
    """Use an LLM to generate relevant tags for an item based on its name and description"""
    A = set()
    for _,row in df.iterrows():
        if 'in' in row['availability'].lower():
            A.add((row['product_name'],row["description"]))
    items = dict(A)
    import google.generativeai as genai
    
    # Configure the Gemini API
    print("Configuring Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set") 
        return []
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.4,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 6000,
        "response_mime_type": "application/json",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )  
    
    # Generate the prompt
    print("Generating prompt...")
    prompt = f"""Generate relevant product tags for the following item dictionary:
    (Name,Description) : {items}

    Return only a JSON object in the following format:
    {{
        "items": [
            {{"name": "item1", "tags": ["tag1", "tag2"]}},
            {{"name": "item2", "tags": ["tag3", "tag4"]}}
        ]
    }}

    Ensure the tags are relevant single-word lowercase attributes focusing on product categories, features, use cases, and key attributes."""

    try:
        print("Generating tags using LLM...")
        response = model.generate_content(prompt)

        print("Processing LLM response...")
        # Ensure the response is valid JSON
        try:
            response_json = json.loads(response.text)
            if "items" not in response_json or not isinstance(response_json["items"], list):
                raise ValueError("Invalid JSON structure in response")

            # Extract item tags into a dictionary
            item_tags_dict = {
                item["name"]: [tag.lower().strip() for tag in item["tags"]]
                for item in response_json["items"]
            }

            print(f"Processed tags for {len(item_tags_dict)} items")
            return item_tags_dict
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
        except Exception as e:
            print(f"Error processing response: {e}")
    except Exception as e:
        print(f"Error generating LLM tags: {e}")

    return {}
def generate_llm_tags_for_current_tags(name,tags):
    """Use an LLM to generate relevant tags for an item based on current tags"""
    print(f"\nGenerating LLM tags : {tags}")
    import google.generativeai as genai
    
    # Configure the Gemini API
    print("Configuring Gemini API...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return []
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    print("Generating prompt...")
    prompt = f"""Restructure relevant product tags based on following tags:
    name: {name}
    Current Tags: {tags}
    
    Return only a comma-separated list of relevant single-word tags in lowercase, with no explanations.
    Focus on product categories, features, use cases, and key attributes."""

    try:
        print("Generating tags using LLM...")
        response = model.generate_content(prompt)
        
        # Extract tags from response and clean them
        print("Processing LLM response...")
        llm_tags = response.text.strip().split(',')
        llm_tags = [tag.strip().lower() for tag in llm_tags]
        
        print(f"Generated {len(llm_tags)} tags: {llm_tags}")
        return llm_tags
    except Exception as e:
        print(f"Error generating LLM tags: {e}")
        return []

# if __name__ == "__main__":
#     # Load product data
#     product_csv = os.getenv("PRODUCT_CSV", "product.csv")
#     df = pd.read_csv(product_csv)
#     print(generate_llm_tags_bulk(df))