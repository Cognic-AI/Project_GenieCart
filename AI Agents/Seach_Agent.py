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

def generate_search_results(prompt,custom_domains):

    print("------------------------------------------------------------------------------------------------")
    print("search agent started")

    tavily_client, gemini_model = initialize_clients()
    
    final_prompt = f""" 
    role: system, content: You are a helpful assistant in Sri Lanka that converts the user prompt into a search query to find products from the web. The products need to be buy from Sri Lanka. You only provide the search query. No other responds.
    role: user, content: {prompt}"""
    response = gemini_model.generate_content(contents=final_prompt)
    search_query = response.text

    print("search_query created: ",search_query)

    tavily_context = tavily_client.search(query=search_query, search_depth="advanced", max_results=30)
    tavily_context_results = []
    for result in tavily_context['results']:
        if 'url' in result:
            tavily_context_results.append(result['url'])

    # Perform searches for each domain
    for domain in custom_domains:
        domain_query = f"{search_query} site:{domain}"  # Restrict search to the domain
        tavily_context = tavily_client.search(query=domain_query, search_depth="advanced", max_results=20)
        
        for result in tavily_context['results']:
            if 'url' in result:
                tavily_context_results.append(result['url'])


    print("tavily_context_results: ", tavily_context_results)

    result_prompt_1 = f""" 
    role: system, content: Analyze the following web page links.Only provide the links that shows many product results not single product pages. This is a must and You only the add links which have {prompt} product mentioned in the link, Other links are not needed. Only give one link from one web domain(Don't give multiple links from same domain/website).Give the results Line by line.
    role: user, content: {tavily_context_results}"""
    response_1 = gemini_model.generate_content(contents=result_prompt_1)

    result_prompt_ = f""" 
    role: system, content: Analyze the following web page links. You must only add the add links which have {prompt} product mentioned in the link, Other links are not needed. Only provide the links that shows many product results not single product pages. Give the results Line by line. Don't add facebook links. Only return 2 links(priorities the {custom_domains} when selecting best links).
    role: user, content: {response_1}"""
    response_ = gemini_model.generate_content(contents=result_prompt_)

    with open("search_agent_output.txt", "w", encoding="utf-8") as f:
        f.write(response_.text)

    print("\n")
    print("search_agent_output.txt created")

    result_prompt_2 = f""" 
    role: system, content: Analyze the following search results and provide the web page links.Only provide the links that shows single product in that web page that is {prompt}. Only return the links line by line.
    role: user, content: {tavily_context_results}"""
    response_2 = gemini_model.generate_content(contents=result_prompt_2)

    with open("Filtered_links.txt", "w", encoding="utf-8") as f:
        f.write(response_2.text)

    print("Filtered_links.txt created")

    print("\n\n")

    print("Search agent completed")
    print("------------------------------------------------------------------------------------------------")

#Example usage
generate_search_results("A4 paper bundle",["https://www.amazon.com","https://daraz.lk"])