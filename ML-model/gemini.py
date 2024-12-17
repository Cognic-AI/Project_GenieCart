import os
import pandas as pd
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
    model = genai.GenerativeModel('gemini-pro')
    
    print("Generating prompt...")
    prompt = f"""Generate relevant product tags for the following item dictionary:
    (Name,Description) : {items}
    
    Return only a list in following format
    [
        (name of the item1, [list of tags for that item1]),
        (name of the item2, [list of tags for that item2]),
    ]
    with relevant single-word tags in lowercase for each item in the dictionary, with no explanations.

    Focus on product categories, features, use cases, and key attributes."""

    try:
        print("Generating tags using LLM...")
        response = model.generate_content(prompt)
        
        # Extract tags from response and clean them
        print("Processing LLM response...")
        # Convert string to list using eval() since response is in list format
        try:
            items_with_tags = eval(response.text)
            # Create dictionary mapping item names to their tags
            item_tags_dict = {}
            for item_name, tags in items_with_tags:
                # Clean the tags - remove quotes and extra characters
                cleaned_tags = [tag.strip("'").strip().lower() for tag in tags]
                item_tags_dict[item_name.strip("'")] = cleaned_tags
            
            print(f"Processed tags for {len(item_tags_dict)} items")
            return item_tags_dict
        except Exception as e:
            print(f"Error processing response: {e}")
            return {}
        return llm_tags
    except Exception as e:
        print(f"Error generating LLM tags: {e}")
        return []

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