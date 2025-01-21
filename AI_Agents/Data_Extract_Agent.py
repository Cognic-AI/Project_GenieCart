import json
import requests
from bs4 import BeautifulSoup, Comment
import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import List, Union, Dict
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time
from typing import Union

# Load environment variables
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

# Initialize Gemini
def initialize_gemini(gemini_api_key: str) -> genai.GenerativeModel:
    """Initializes the Gemini API with the provided API key."""
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    generation_config: dict = {
        "temperature": 0.1,
        "top_p": 0.6,
        "top_k": 10,
        "max_output_tokens": 20000,
        "response_mime_type": "application/json",
    }
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

def find_relevant_sections(soup: BeautifulSoup, request_id: str) -> Dict[str, str]:
    """Find relevant sections using vector similarity search."""
    
    # Save entire soup to text file and read content
    with open(f'webpage_content_{request_id}.txt', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    with open(f'webpage_content_{request_id}.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Delete the temporary file
    os.remove(f'webpage_content_{request_id}.txt')
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english'
    )
    
    # Create document vector from the entire content
    doc_vector = vectorizer.fit_transform([content])
    
    relevant_sections = {}
    # Group similar search terms together
    term_groups = {
        'name': ['product name', 'product title', 'item name', 'item title'],
        'description': ['description', 'product details', 'item details', 'about this item'],
        'price': ['price', 'cost', 'sale price', 'regular price', 'current price'],
        'rating': ['rating', 'reviews', 'customer reviews', 'star rating', 'product rating'],
        'shipping': ['shipping', 'delivery', 'shipping options', 'delivery options', 'shipping details'],
        'availability': ['availability', 'stock', 'in stock', 'out of stock', 'inventory status'],
        'warranty': ['warranty', 'guarantee', 'product warranty', 'warranty information'],
        'image': ['image', 'product image', 'item image', 'gallery'],
        'currency': ['currency', 'price currency', 'money']
    }

    # Process each group of related terms
    for group_key, terms in term_groups.items():
        max_similarity = 0
        best_text = []
        
        for term in terms:
            query_vector = vectorizer.transform([term])
            similarity = cosine_similarity(query_vector, doc_vector)[0][0]
            
            if similarity > max_similarity:
                max_similarity = similarity
                sections = content.split('\n')
                matching_indices = [i for i, section in enumerate(sections) if term.lower() in section.lower()]
                
                best_text = []
                for idx in matching_indices:
                    start_idx = max(0, idx - 1) 
                    end_idx = min(len(sections), idx + 2) 
                    context = sections[start_idx:end_idx]
                    best_text.extend([s.strip() for s in context])
        if max_similarity > 0.01 and best_text:
            # For price, validate it contains actual price information
            if group_key == 'price':
                # Check if text contains numeric values and currency symbols
                api_key: str = key_manager.get_next_key()
                gemini_model: genai.GenerativeModel = initialize_gemini(api_key)
                prompt: str = f"""
                Check the following text has price correct or not 
                return true or false only (true for correct and false for incorrect)
                {best_text} 
                """
                try:
                    response = gemini_model.generate_content(contents=prompt)
                    if response.text != "false":
                        print(f"Price is correct")
                        relevant_sections[group_key] = "\n".join(best_text)
                    else:
                        relevant_sections[group_key] = "null"
                        print(f"Price is not correct")
                except Exception as e:
                    print(f"Error validating price: {e}")
                    relevant_sections[group_key] = "null"
            else:
                relevant_sections[group_key] = "\n".join(best_text)
        else:
            relevant_sections[group_key] = "null"
    return relevant_sections

# Function to extract all visible text from a webpage
def extract_page_content(url: str, country_code: str, latitude: float = None, longitude: float = None) -> Union[str, BeautifulSoup]:
    """Extracts and parses the content of a webpage."""
    try:
        headers: dict = {
            "User-Agent": os.getenv("USER_AGENT"),
            "Accept-Language": "en-US,en;q=0.9",
            "geo-location": country_code
        }
        
        # Add geolocation headers if coordinates provided
        if latitude is not None and longitude is not None:
            headers.update({
                "geo-position": f"{latitude};{longitude}",
                "geo-coordinates": f"{latitude}, {longitude}"
            })
            
        response: requests.Response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML using BeautifulSoup
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
            
        return soup

    except Exception as e:
        return f"Error extracting content from {url}: {e}"
    
# Function to extract all visible text from a webpage
def extract_amazon_page_content(url: str, country_code: str, latitude: float = None, longitude: float = None) -> Union[str, BeautifulSoup]:
    """Extracts and parses the content of a webpage."""
    try:
        headers: dict = {
            "User-Agent": os.getenv("USER_AGENT"),
            "Accept-Language": "en-US,en;q=0.9",
            "geo-location": country_code,
            "Accept-Location": country_code

        }

        # Add geolocation headers for Canada
        if country_code == "CA":
            headers.update({
                "CF-IPCountry": "CA",
                "X-Forwarded-For": "24.48.0.1",  # Canadian IP address
                "geo-position": f"{latitude};{longitude}",  # Toronto coordinates
                "geo-coordinates": f"{latitude}, {longitude}",
                "X-Geo-Position": f"{latitude}, {longitude}",
                "X-Geo-Location": "CA"
            })
            
        response: requests.Response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML using BeautifulSoup
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        text = ""
        
        # Extract product title
        product_title = soup.find('span', {'id': 'productTitle'})
        if product_title:
            product_title = product_title.text.strip()
        text += "product_title: " + product_title
        text += "\n\n"
            
        # Extract product description
        description_list = soup.find('ul', {'class': 'a-unordered-list a-vertical a-spacing-mini'})
        if description_list:
            description_items = description_list.find_all('span', {'class': 'a-list-item'})
            description_text = ' '.join([item.text.strip() for item in description_items])
            text += "description: " + description_text
            text += "\n\n"

        # Extract rating
        rating_element = soup.find('span', {'data-hook': 'rating-out-of-text', 'class': 'a-size-medium a-color-base'})
        if rating_element:
            rating = rating_element.text.strip()
            text += "rating: " + rating
            text += "\n\n"

        # Extract availability
        availability_element = soup.find('div', {'id': 'availability'})
        if availability_element:
            availability = availability_element.find('span', {'class': 'a-size-medium a-color-success'})
            if availability:
                availability_text = availability.text.strip()
                text += "availability: " + availability_text
            text += "\n\n"

        # Extract price and currency
        price_whole = soup.find('span', {'class': 'a-price-whole'})
        price_decimal = soup.find('span', {'class': 'a-price-decimal'})
        price_fraction = soup.find('span', {'class': 'a-price-fraction'})
        currency_symbol = soup.find('span', {'class': 'a-price-symbol'})
        
        if price_whole and currency_symbol:
            price = price_whole.text.strip()
            if price_decimal and price[-1] != ".":
                price += price_decimal.text.strip()
            price += price_fraction.text.strip()
            currency = currency_symbol.text.strip()
            text += "price: " + price
            text += "currency: " + currency
            text += "\n\n"

        # Extract product image
        image_element = soup.find('img', {'id': 'landingImage'})
        if image_element:
            image_url = image_element.get('src')
            if image_url:
                text += "image: " + image_url
                text += "\n\n"

        # Extract reviews
        reviews = []
        review_elements = soup.find_all('div', {'data-hook': 'review-collapsed'})
        for review in review_elements:
            review_text = review.find('span')
            if review_text:
                reviews.append(review_text.text.strip())
        
        if reviews:
            text += "reviews: " + str(reviews)
            text += "\n\n"
        # Extract all content from elements containing a-box-group in their class
        box_groups = soup.find_all(lambda tag: tag.get('class') and 'a-box-group' in tag.get('class'))
        if box_groups:
            box_contents = []
            for box in box_groups:
                # Get all text content from the box, preserving line breaks
                lines = [line.strip() for line in box.stripped_strings]
                box_contents.extend(lines)
            
            if box_contents:
                text += "box_contents: " + ", ".join(box_contents)
                text += "\n\n"

        return text

    except Exception as e:
        return f"Error extracting content from {url}: {e}"
    
# Process each link and save responses in separate files
def process_links(country_code: str, custom_domains: List[str], location: List[float], request_id: str) -> None:
    """Processes each link and saves structured responses in separate files."""
    print("------------------------------------------------------------------------------------------------")
    print("Data extraction agent started")

    input_filename: str = os.path.join("Agent_Outputs", f"Filtered_links_{request_id}.txt")
    with open(input_filename, "r", encoding="utf-8") as f:
        links: List[str] = [line.strip() for line in f.readlines() if line.strip()]

    # Variable to keep track of the product number
    product_counter: int = 1

    # Clear the folder
    folder_path = os.path.join("Final_products",f"Final_products_{request_id}")

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Remove the folder and its contents
    os.makedirs(folder_path, exist_ok=True)  # Recreate the folder

    for link in links:
        print(f"Processing: {link}")
        try:
            if custom_domains == ["https://www.amazon.com"]:
                page_content: Union[str, BeautifulSoup] = extract_amazon_page_content(link,country_code,location[0],location[1])
                relevant_content = page_content
            else:
                page_content: Union[str, BeautifulSoup] = extract_page_content(link,country_code,location[0],location[1])
                # Find relevant sections using vector similarity search
                relevant_sections = find_relevant_sections(page_content, request_id)
                if relevant_sections.get('price') == "null":
                    print(f"Price is not available for {link}")
                    continue
                # Combine relevant sections into a single string
                relevant_content = "\n".join([f"{term}: {content}" for term, content in relevant_sections.items()])

            # Get the next API key and initialize Gemini model
            api_key: str = key_manager.get_next_key()
            gemini_model: genai.GenerativeModel = initialize_gemini(api_key)

            # Send the content to Gemini for structuring
            prompt: str = f"""
            You are a product data extraction specialist. Analyze the provided HTML content and structure the product details into a clean JSON format.

            Rules:
            - Only extract data if the product ships to {country_code}. If not available, return an empty JSON object.
            - Price is the most important field and should be extracted.
            - For prices, always include the final price after any discounts. Never leave price as null.
            - Product ratings should be on a 0-5 scale with one decimal place.
            - For boolean fields (availability, shipping, warranty), use strict true/false values.
            - Extract up to 10 most recent customer reviews.
            - All text fields should be properly cleaned of HTML tags and special characters.

            Add the following fields to the JSON:
            product_url
            product_name
            description
            price (There can be previous price and price after discounts add the after discount price)
            currency
            product_rating (Mostly this is available which is usually 0 to 5 find the rating and add it)
            availability(make false if mentioned as out of stock otherwise always true)
            shipping (if mentioned as not shipping to {country_code}, mention false otherwise always true)
            delivery_date (add the delivery date or how long it takes to deliver only for {country_code})
            delivery_cost(or shipping cost only for {country_code})
            warranty(true or false on availability)
            image(add the image url)
            latest_reviews(The reviews are available in the bottom parts analyze and add them)

            URL: {link}
            Relevant Content: {relevant_content}
            """
            
            response = gemini_model.generate_content(contents=prompt)

            # Write new files
            filename = os.path.join(folder_path, f"product{product_counter}.json")
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(response.text)
            print(f"Saved response to: {filename}")

            product_counter += 1

            if product_counter == 32:
                break

        except Exception as e:
            print(f"Error processing {link}: {str(e)}")

    print("Data extraction agent completed")
    print("------------------------------------------------------------------------------------------------")

# Helper function to sanitize file names
def sanitize_filename(url: str) -> str:
    """Sanitizes the URL to create a valid file name."""
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in url)

# Example usage
# start_time = time.time()
# process_links("CA",None,[56.4383657,-114.8492314],"1234567898")
# process_links("CA",["https://www.amazon.com"],[56.4383657,-114.8492314],"1234567899")
# end_time = time.time()
# print(f"Time taken: {end_time - start_time:.2f} seconds")