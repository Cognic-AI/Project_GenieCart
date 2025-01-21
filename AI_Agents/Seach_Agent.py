import os
from dotenv import load_dotenv
from tavily import Client as TavilyClient
import google.generativeai as genai
from typing import List

load_dotenv()

def initialize_clients() -> tuple[TavilyClient, genai.GenerativeModel]:
    """
    Initialize and return the Tavily and Gemini clients.
    Returns a tuple containing:
    - TavilyClient instance
    - Gemini GenerativeModel instance
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")
    tavily_client = TavilyClient(tavily_api_key)
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 4096,
        "response_mime_type": "text/plain",
    }
    
    gemini_model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )  
    
    return tavily_client, gemini_model

def generate_search_results(prompt: str, custom_domains: List[str],tags: List[str],country_code: str,request_id: str) -> None:
    """
    Generate search results for a given prompt, restricting to the provided domains.
    
    Args:
    - prompt (str): The search prompt to generate queries for.
    - custom_domains (List[str]): A list of domains to restrict the search to.
    - tags A list of tags to be used in the search.
    - country_code The country code where the products searched.
    - request_id A unique identifier for this specific search task.
    Returns:
    - None
    """
    print("------------------------------------------------------------------------------------------------")
    print("search agent started")

    # Create Agent_Outputs directory if it doesn't exist
    os.makedirs("Agent_Outputs", exist_ok=True)

    tavily_client, gemini_model = initialize_clients()
    
    final_prompt = f""" 
    role: system, content: You are a helpful assistant that converts the user prompt into a search query to find products from {country_code} using web search. You only provide the search query. In the search query mention as buy from the given country(convert the country code to country name). No other responds.
    role: user, content: {prompt}, tags: {tags}"""
    response = gemini_model.generate_content(contents=final_prompt)
    search_query = response.text

    print("search_query created: ", search_query)

    tavily_context_results = []
    
    # If custom domains provided, only search those domains
    if custom_domains:
        for domain in custom_domains:
            domain_query = f"{search_query} site:{domain} location:{country_code}"
            tavily_context = tavily_client.search(query=domain_query, search_depth="advanced", max_results=20)
            
            for result in tavily_context['results']:
                if 'url' in result:
                    tavily_context_results.append(result['url'])
    else:
        # If no custom domains, do a general search
        tavily_context = tavily_client.search(query=f"{search_query} location:{country_code}", search_depth="advanced", max_results=50, exclude_domains = ["https://www.facebook.com"])
        for result in tavily_context['results']:
            if 'url' in result:
                tavily_context_results.append(result['url'])

    print("tavily_context_results: ", tavily_context_results)

    result_prompt_1 = f""" 
    role: system, content: You are a search results analyzer for {country_code}. Your task is to filter product listing pages that contain multiple items matching '{prompt}'. Rules:
    1. Only include links to category pages, search results pages, or collection pages
    2. The page URL must contain keywords related to {prompt}
    3. Exclude any single product pages or irrelevant category pages
    4. If no links meet these criteria, return null
    5. Return valid links one per line with no additional text or commentary
    role: user, content: {tavily_context_results}"""
    response_1 = gemini_model.generate_content(contents=result_prompt_1)

    # result_prompt_ = f""" 
    # role: system, content: Analyze the following web page links from {country_code}. You must only add the add links which have {prompt} product mentioned in the link, Other links are not needed. If you think this link will give more unrelated results, don't add it. Give the results Line by line.
    # role: user, content: {response_1}"""
    # response_ = gemini_model.generate_content(contents=result_prompt_)

    filename: str = os.path.join("Agent_Outputs", f"search_agent_output_{request_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response_1.text)

    print("\n")
    print("search_agent_output.txt created")

    result_prompt_2 = f""" 
    role: system, content: You are a product link analyzer. Your task is to analyze search results from {country_code} and identify ONLY direct product pages for {prompt}. Rules:
    1. Only include links that lead directly to a single product page
    2. The product on that page must exactly match {prompt} - no variations or similar items
    3. Exclude category pages, search results pages, or marketplace listings with multiple items
    4. If no links meet these criteria, return null
    5. Return valid links one per line with no additional text
    role: user, content: {tavily_context_results}"""
    response_2 = gemini_model.generate_content(contents=result_prompt_2)

    filename: str = os.path.join("Agent_Outputs", f"Filtered_links_{request_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response_2.text)

    print("Filtered_links.txt created")

    print("\n\n")

    print("Search agent completed")
    print("------------------------------------------------------------------------------------------------")

# Example usage
generate_search_results("Tomato Ketchup",None,["Tomato","Ketchup"],"US","1234567890")
# generate_search_results("Tomato Ketchup", ["https://www.amazon.com"],["Tomato","Ketchup","Quality"],"CA","1234567890")
