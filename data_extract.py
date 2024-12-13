from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Configure WebDriver (using Chrome as an example)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Function to scrape product details from an individual product page
def scrape_product_page():
    try:
        # Extract product name
        title = driver.find_element(By.CSS_SELECTOR, "h1.pdp-mod-product-badge-title").text
        # Extract product price
        price = driver.find_element(By.CSS_SELECTOR, "span.pdp-price").text
        # Extract product brand
        brand = driver.find_element(By.CSS_SELECTOR, "a.pdp-product-brand__brand-link").text
        return {"Title": title, "Price": price, "Brand": brand}
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
def scrape_products(search_term, num_results=3):
    base_url = "https://www.daraz.lk/"
    driver.get(base_url)

    # Search for the product
    search_box = driver.find_element(By.CSS_SELECTOR, "input#q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to be visible (not waiting for the full page load)
    time.sleep(2)  # Small fixed wait time for the search results to load

    # Get product links
    product_links = get_product_links()
    product_links = product_links[:num_results]  # Limit to first 3 products

    # Extract details for each product
    products = []
    for link in product_links:
        driver.get(link)
        time.sleep(2)  # Small fixed wait time for the product page to load
        product_details = scrape_product_page()
        if product_details:
            products.append(product_details)

        # Go back to the search results page
        driver.back()
        time.sleep(2)  # Wait a bit before interacting with the search results page again

    return pd.DataFrame(products)

# Example usage
if __name__ == "__main__":
    search_term = "wireless headphones"
    results = scrape_products(search_term)
    print(results)

    # Save results to a CSV file
    results.to_csv("product_results.csv", index=False)

    # Quit the WebDriver
    driver.quit()


