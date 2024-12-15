from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure WebDriver (using Chrome as an example)
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument(f"user-agent={os.getenv('USER_AGENT')}")
# options.add_argument('--headless')  # Uncomment for headless mode
driver = webdriver.Chrome(options=options)

def initialize_gemini():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 10000,
        "response_mime_type": "text/plain",
    }
    
    gemini_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )  
    
    return gemini_model

# Function to scroll the page slowly
def slow_scroll_page():
    """Scroll down the webpage slowly to load dynamic content."""
    scroll_pause_time = 1  # Time to wait between scrolls (adjust as needed)
    scroll_height_increment = 300  # Pixels to scroll in each step

    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0

    while current_position < total_height:
        # Scroll down by the increment
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        current_position += scroll_height_increment
        time.sleep(scroll_pause_time)  # Wait for the page to load more content

        # Update the total height (to handle dynamically loaded content)
        total_height = driver.execute_script("return document.body.scrollHeight")

# Function to extract all links from a webpage
def extract_all_links(url,item_name):
    driver.get(url)

    # Wait for the page to initially load
    time.sleep(5)

    # Scroll the page to load all dynamic content
    slow_scroll_page()

    # Find all <a> tags with href attributes
    elements = driver.find_elements(By.TAG_NAME, "a")
    all_links = []
    for element in elements:
        href = element.get_attribute("href")
        if href:  # Check if the href attribute is not empty
            all_links.append(href)

    # Deduplicate links
    unique_links = list(set(all_links))

    driver.quit()

    gemini_model = initialize_gemini()

    chat_session = gemini_model.start_chat()

    final_prompt = f""" 
    role: system, content: You are a helpful assistant to filter the given product links and return only the links which are related to the item name. Return the full link with the website. Return line by line. Make sure you return only the links that related to a one spesific item.(Analyse the link and get a understanding of it)
    role: user, content: website {url} \n\n item name {item_name} \n\n links \n\n {unique_links}"""

    response = chat_session.send_message(final_prompt)

    # Save Gemini's response to a text file line by line
    with open("Filtered_links.txt", "a", encoding="utf-8") as f:
        f.write(response.text)



item_name = "canon f166400 printer ink cartridge"
url = "https://www.amazon.com/s?k=canon+f166400+printer+ink+cartridge&crid=3NCB1LF193ACW&sprefix=%2Caps%2C1034&ref=nb_sb_ss_recent_2_0_recent"

extract_all_links(url,item_name)