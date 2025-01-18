from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Step 1. Instantiating your TavilyClient
load_dotenv()
tavily_api = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api)


# Step 2. Defining the list of URLs to extract content from
urls = [
    "https://www.amazon.com/Georgia-Olive-Farms-Extra-Virgin/dp/B07641GK6H"]

# Step 3. Executing the extract request
response = tavily_client.extract(urls=urls, include_images=True)

# Step 4. Printing the extracted raw content
for result in response["results"]:
    print(f"URL: {result['url']}")
    print(f"Raw Content: {result['raw_content']}")
    print(f"Images: {result['images']}\n")

# Note that URLs that could not be extracted will be stored in response["failed_results"]
