import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini
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
    }
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

gemini_model = initialize_gemini()

# Function to extract all visible text from a webpage
def extract_page_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # # Extract all visible text (excluding script and style tags)
        # for script in soup(["script", "style"]):
        #     script.extract()  

        # visible_text = soup.get_text(separator="\n").strip()
        return soup
    except Exception as e:
        return f"Error extracting content from {url}: {e}"

# Process each link and send data to Gemini
def process_links(input_file, output_file):
    # Read links from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines() if line.strip()]

    # Open the output file to save results
    with open(output_file, "a", encoding="utf-8") as out_file:
        for link in links:
            print(f"Processing: {link}")
            try:
                # Extract page content
                page_content = extract_page_content(link)

                # Send the content to Gemini for structuring
                chat_session = gemini_model.start_chat()
                prompt = f"""
                Structure the following product details from the webpage html in JSON format:

                URL: {link}
                Content: {page_content}
                """
                response = chat_session.send_message(prompt)

                # Write the structured response to the output file
                out_file.write(f"URL: {link}\n")
                out_file.write(f"{response.text}\n")
                out_file.write("=" * 80 + "\n")
            except Exception as e:
                print(f"Error processing {link}: {e}")
                out_file.write(f"URL: {link}\nError: {e}\n")
                out_file.write("=" * 80 + "\n")

# Main function
if __name__ == "__main__":
    input_file = "testlinks.txt"  # File containing the links
    output_file = "structured_product_details.txt"  # File to save structured data
    process_links(input_file, output_file)
