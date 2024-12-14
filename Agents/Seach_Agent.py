import os
import asyncio
from dotenv import load_dotenv
from tavily import Client as TavilyClient
import google.generativeai as genai

load_dotenv()

def initialize_clients():
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")
    tavily_client = TavilyClient(tavily_api_key)
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    genai.configure(api_key=gemini_api_key)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 4096,
        "response_mime_type": "text/plain",
    }
    
    gemini_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )  
    
    return tavily_client, gemini_model

def generate_response(prompt):

    tavily_client, gemini_model = initialize_clients()
    
    chat_session = gemini_model.start_chat()
    final_prompt = f""" 
    role: system, content: You are a helpful assistant in Sri Lanka that converts the user prompt into a search query to find products. You only provide the search query. No other responds.
    role: user, content: {prompt}"""
    response = chat_session.send_message(final_prompt)
    search_query = response.text

    print(search_query)

    tavily_context = tavily_client.search(query=search_query, search_depth="advanced", max_results=10)
    tavily_context_results = []
    for result in tavily_context['results']:
        if 'url' in result:
            tavily_context_results.append(result['url'])


    custom_domains = ["https://www.amazon.com", "https://www.aliexpress.com"]  # Replace with your desired domains

    # Perform searches for each domain
    for domain in custom_domains:
        domain_query = f"{search_query} site:{domain}"  # Restrict search to the domain
        tavily_context = tavily_client.search(query=domain_query, search_depth="advanced", max_results=10)
        
        for result in tavily_context['results']:
            if 'url' in result:
                tavily_context_results.append(result['url'])


    print(tavily_context_results)
    print("\n\n")

    result_prompt = f""" 
    role: system, content: Analyze the following search results and provide the web page links of each result.Line by line numbered.Don't duplicate the same links.    
    role: user, content: {tavily_context_results}"""
    response = chat_session.send_message(result_prompt)

    return response.text


print(generate_response("Type c usb cable"))