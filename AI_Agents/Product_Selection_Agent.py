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
        model_name="gemini-1.5-pro",
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

def extract_all_links(item_name: str, custom_domains: List[str], country_code: str, location: List[float], request_id: str) -> None:
    """
    Extracts all product links by searching for the item name on given websites, handling various website structures.

    Args:
    - item_name (str): The name of the item to search for.
    - country_code (str): The country code where the products searched.
    - request_id (str): A unique identifier for this specific product selection task.

    Returns:
    - None
    """
    # Configure WebDriver (using Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument(f"user-agent={os.getenv('USER_AGENT')}")
    options.add_argument(f'--geo-location={country_code}')  # Set geolocation 
    options.add_argument('--headless')

    print("------------------------------------------------------------------------------------------------")
    print("Product selection agent started")

    input_filename: str = os.path.join("Agent_Outputs", f"search_agent_output_{request_id}.txt")
    with open(input_filename, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines() if line.strip()][:3]

    for link in links:
        driver = webdriver.Chrome(options=options)
        
        # Set geolocation coordinates
        latitude = location[0]
        longitude = location[1]
        accuracy = 100
        
        driver.maximize_window()
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy
        })
        
        print(f"Processing link: {link}")
        driver.get(link)

        # Wait for the page to initially load
        time.sleep(5)

        # Scroll the page to load all dynamic content
        slow_scroll_page(driver)

        all_links = []
        
        # Special handling for Amazon
        if custom_domains == ["https://www.amazon.com"]:
            elements = driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal")
            for element in elements:
                href = element.get_attribute("href")
                if href:
                    all_links.append(href)
        else:
            # Default handling for other websites
            elements = driver.find_elements(By.TAG_NAME, "a")
            for element in elements:
                href = element.get_attribute("href")
                if href:  # Check if the href attribute is not empty
                    all_links.append(href)

        # Deduplicate links
        unique_links = list(set(all_links))

        driver.quit()

        print(f"Extracted {len(unique_links)} links from {link}")

        gemini_model = initialize_gemini()

        final_prompt = f"""
            role: system, content: You are a helpful assistant to filter the given product links and return only the links which are related to the item name and from {country_code}. Return the full link with the website. Return line by line. Make sure you return only the links that are related to a one specific item (Analyze the link and get an understanding of it).   
            role: user, content: website {link} \n\n item name {item_name} \n\n links \n\n {unique_links}"""

        if custom_domains == ["https://www.amazon.com"]:
            final_links = unique_links
        else:
            response = gemini_model.generate_content(contents=final_prompt)
            final_links = response.text

        output_filename: str = os.path.join("Agent_Outputs", f"Filtered_links_{request_id}.txt")
        with open(output_filename, "a", encoding="utf-8") as f:
            # Convert list to string if needed
            if isinstance(final_links, list):
                final_links = "\n".join(final_links)
            f.write(final_links)

        print(f"Filtered links saved to: {output_filename}")

    print("Product selection agent completed")
    print("------------------------------------------------------------------------------------------------")

# Example usage
# start_time = time.time()
# extract_all_links("Water bottle", None, "CA", [56.4383657,-114.8492314], "1234567898")
# extract_all_links("Water bottle", ["https://www.amazon.com"], "CA", [56.4383657,-114.8492314], "1234567899") 
# end_time = time.time()
# print(f"Time taken: {end_time - start_time:.2f} seconds")