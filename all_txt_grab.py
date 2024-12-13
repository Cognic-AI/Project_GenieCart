from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configure WebDriver (using Chrome as an example)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Function to extract all visible text from the page
def extract_all_text_from_page():
    try:
        # Get the text content of the entire page
        page_text = driver.find_element(By.TAG_NAME, "body").text
        return page_text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

# Function to scrape product links from the search results page
def get_product_links():
    product_cards = driver.find_elements(By.CSS_SELECTOR, "div.Bm3ON")
    product_links = []
    for card in product_cards:
        try:
            link_element = card.find_element(By.CSS_SELECTOR, "a")
            product_links.append(link_element.get_attribute("href"))
        except Exception as e:
            print(f"Error extracting product link: {e}")
    return product_links

# Main function to scrape products for a search term
def scrape_products(search_term, num_results=5):
    base_url = "https://www.daraz.lk/"
    driver.get(base_url)

    # Search for the product
    search_box = driver.find_element(By.CSS_SELECTOR, "input#q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results page to load
    time.sleep(3)

    # Get product links
    product_links = get_product_links()
    product_links = product_links[:num_results]

    # Extract all text from each product page
    all_page_text = []
    for link in product_links:
        driver.get(link)
        time.sleep(3)  # Wait for the product page to load
        page_text = extract_all_text_from_page()
        if page_text:
            all_page_text.append(page_text)

    return all_page_text

# Example usage
if __name__ == "__main__":
    search_term = "wireless headphones"
    all_text_data = scrape_products(search_term)

    # Save all the extracted text content to a text file
    with open("product_text_details.txt", "w", encoding="utf-8") as f:
        for text in all_text_data:
            f.write(text)
            f.write("\n" + "="*80 + "\n")  # Separate products with a line

    # Quit the WebDriver
    driver.quit()
