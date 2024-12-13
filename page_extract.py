from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure WebDriver (using Chrome as an example)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Function to scrape all details from the product page
def scrape_product_page(product_link):
    try:
        # Go to the product page
        driver.get(product_link)
        time.sleep(3)  # Wait for the product page to load
        
        # Get the entire page content as text
        page_content = driver.page_source
        
        # Optionally, you can extract more structured data from the page if needed
        # Here we are capturing all HTML content for the page
        
        return page_content
    except Exception as e:
        print(f"Error extracting product details: {e}")
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
def scrape_products(search_term, num_results=1):
    base_url = "https://www.daraz.lk/"
    driver.get(base_url)

    # Search for the product
    search_box = driver.find_element(By.CSS_SELECTOR, "input#q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.Bm3ON"))
    )

    # Get product links
    product_links = get_product_links()
    product_links = product_links[:num_results]

    # Extract details for each product
    all_product_data = []
    for link in product_links:
        page_content = scrape_product_page(link)
        if page_content:
            all_product_data.append(page_content)

    return all_product_data

# Example usage
if __name__ == "__main__":
    search_term = "wireless headphones"
    all_data = scrape_products(search_term)

    # Save all the scraped product page content to a text file
    with open("product_details.txt", "w", encoding="utf-8") as f:
        for data in all_data:
            f.write(data + "\n\n" + "="*80 + "\n\n")

    # Quit the WebDriver
    driver.quit()
