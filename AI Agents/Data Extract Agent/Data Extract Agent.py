import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini with API key cycling
class GeminiKeyManager:
    def __init__(self):
        self.api_keys = [
            os.getenv("GEMINI_API_KEY_1"),
            os.getenv("GEMINI_API_KEY_2"),
            os.getenv("GEMINI_API_KEY_3"),
            os.getenv("GEMINI_API_KEY_4"),
        ]
        if not all(self.api_keys):
            raise ValueError("One or more GEMINI_API_KEYS are missing from environment variables.")
        self.current_index = 0

    def get_next_key(self):
        key = self.api_keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.api_keys)
        return key

key_manager = GeminiKeyManager()

# Initialize Gemini
def initialize_gemini(gemini_api_key):
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.6,
        "top_k": 10,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

# Function to extract all visible text from a webpage
def extract_page_content(url):
    try:
        headers = {
            "User-Agent": os.getenv("USER_AGENT"),
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        return soup
    except Exception as e:
        return f"Error extracting content from {url}: {e}"

# Process each link and save responses in separate files
def process_links(input_file, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read links from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines() if line.strip()]

    for link in links:
        print(f"Processing: {link}")
        try:
            # Extract page content
            page_content = extract_page_content(link)

            # Get the next API key and initialize Gemini model
            api_key = key_manager.get_next_key()
            print(f"Using API key: {api_key}")
            gemini_model = initialize_gemini(api_key)

            # Send the content to Gemini for structuring
            prompt = f"""
            Structure the following product details in JSON format from the webpage html content:
            Add the following fields to the JSON:
            product URL
            product_name
            description
            brand
            category
            price 
            currency
            product rating
            Color (all colors available)
            product_qty
            shipping (if shipping is available)
            delivery (delivery details)
            warranty
            warranty_policy
            availability
            condition
            image
            latest reviews

            URL: {link}
            HTML Content: {page_content}
            """
            response = gemini_model.generate_content(contents=prompt)

            # Save the structured response to a separate file
            filename = os.path.join(output_folder, f"{sanitize_filename(link)}.json")
            with open(filename, "w", encoding="utf-8") as out_file:
                out_file.write(response.text)
            print(f"Saved response to: {filename}")

        except Exception as e:
            print(f"Error processing {link}: {e}")

# Helper function to sanitize file names
def sanitize_filename(url):
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in url)

# Main function
if __name__ == "__main__":
    input_file = "testlinks.txt"  # File containing the links
    output_folder = "structured_responses"  # Folder to save responses
    process_links(input_file, output_folder)
