import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

def initialize_gemini():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 4096,
        "response_mime_type": "application/json",
    }
    
    gemini_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )  
    
    return gemini_model

def extract_product_links(url,item_name):
    # Step 1: Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status Code: {response.status_code}")
        return []

    # Step 2: Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)

    # Step 3: Extract product links
    links = []
    for product_card in soup.select('a'):  # Modify 'a' with the specific selector if needed
        link = product_card.get('href')
        links.append(link)

    gemini_model = initialize_gemini()

    chat_session = gemini_model.start_chat()

    final_prompt = f""" 
    role: system, content: You are a helpful assistant to filter the given product links and return only the links which are related to the item name in JSON format. Return the full link with the website.
    role: user, content: links {links} , item name {item_name} , website {url}"""

    # print(final_prompt)
    response = chat_session.send_message(final_prompt)

    return response.text

# Example Usage
url = "https://www.aliexpress.com/w/wholesale-USB-C-cable.html"
item_name = "USB Type C Cable"
product_links = extract_product_links(url,item_name)

# Display or pass the product links to Gemini for further processing
print("Extracted Product Links:")
print(product_links)