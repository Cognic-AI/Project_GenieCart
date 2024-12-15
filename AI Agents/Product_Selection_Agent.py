from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

def initialize_gemini() -> genai.GenerativeModel:
    """
    Initializes the Gemini model with the API key and configuration.
    
    Returns:
    - A configured Gemini GenerativeModel instance.
    """
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

def slow_scroll_page(driver: webdriver.Chrome) -> None:
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

def extract_all_links(item_name: str) -> None:
    """
    Extracts all product links from the search results based on the item name.
    
    Args:
    - item_name (str): The name of the item to search for.

    Returns:
    - None
    """
    # Configure WebDriver (using Chrome as an example)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument(f"user-agent={os.getenv('USER_AGENT')}")
    # options.add_argument('--headless')  
    driver = webdriver.Chrome(options=options)

    print("------------------------------------------------------------------------------------------------")
    print("Product selection agent started")

    with open("search_agent_output.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines() if line.strip()]

    for link in links:
        driver.get(link)

        # Wait for the page to initially load
        time.sleep(5)

        # Scroll the page to load all dynamic content
        slow_scroll_page(driver)

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

        print("links extracted")

        gemini_model = initialize_gemini()

        final_prompt = f""" 
        role: system, content: You are a helpful assistant to filter the given product links and return only the links which are related to the item name. Return the full link with the website. Return line by line. Make sure you return only the links that related to a one specific item.(Analyse the link and get a understanding of it)
        role: user, content: website {link} \n\n item name {item_name} \n\n links \n\n {unique_links}"""

        response = gemini_model.generate_content(contents=final_prompt)

        print("filtered links")

        print("\n\n")

        print("Product selection agent completed")
        print("------------------------------------------------------------------------------------------------")

        # Save Gemini's response to a text file line by line
        with open("Filtered_links.txt", "a", encoding="utf-8") as f:
            f.write(response.text)

# Example usage
# extract_all_links("canon f166400 printer ink cartridge")
