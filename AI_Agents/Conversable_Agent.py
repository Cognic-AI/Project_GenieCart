from autogen import ConversableAgent
import sys
import uuid
import os
from dotenv import load_dotenv
from AI_Agents.Seach_Agent import generate_search_results
from AI_Agents.Product_Selection_Agent import extract_all_links
from AI_Agents.Data_Extract_Agent import process_links
from AI_Agents.Data_frame_creator_Agent import json_to_csv

load_dotenv()

entrypoint_agent_system_message=""" 
You are the supervisor agent coordinating multiple sub-agents to fulfill user queries efficiently. Ensure each sub-agent executes tasks correctly in sequence: search, product selection, and data extraction.
"""

search_agent_system_message = """
You are responsible for executing the `generate_search_results` function.
This function takes four inputs:
- `user_query`: A string representing the product or item to search for.
- `custom_domains`: A list of domains where the search should be restricted.
- `tags`: A list of tags to be used in the search.
- `country_code`: The country code where the products searched. 
- `request_id`: A unique identifier for this specific search task.
"""


product_selection_agent_system_message = """
Your task is to execute the `extract_all_links` function when invoked. 
This function takes one input:
- A string representing the product or item name.
- A string representing the country code where the products searched.
- A list representing the location of the user.
- A string representing the request ID for this specific product selection task.

Execute the function with the given input and ensure it runs successfully.
"""

data_extract_agent_system_message=""" 
Your task is to execute the `process_links` function when invoked.
This function takes one input:
- A string representing the country code where the products searched.
- A string representing the request ID for this specific data extraction task.
Execute the function and ensure it runs successfully.
"""

data_frame_creator_agent_system_message="""
Your task is to execute the `json_to_csv` function when invoked.
This function takes one input:
- A string representing the product or item name.
- A string representing the country code.
- A string representing the request ID for this specific data frame creation task.

Execute the function and ensure it runs successfully.
"""

def main(user_query, custom_domains,tags,country_code,location,request_id):
    print("user_query")
    print(user_query)
    print("custom_domains")
    print(custom_domains)
    print("tags")
    print(tags)
    print("country_code")
    print(country_code)
    print("location")
    print(location)
    print("request_id")
    print(request_id)
    llm_config = {
        "config_list": [
            {"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}
        ]
    }

    # Main entrypoint/supervisor agent
    entrypoint_agent = ConversableAgent(
        name=f"entrypoint_agent_{request_id}",
        system_message=entrypoint_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    entrypoint_agent.register_for_execution(name="generate_search_results")(generate_search_results)
    entrypoint_agent.register_for_execution(name="extract_all_links")(extract_all_links)
    entrypoint_agent.register_for_execution(name="process_links")(process_links)
    entrypoint_agent.register_for_execution(name="json_to_csv")(json_to_csv)

    # Search agent
    search_agent = ConversableAgent(
        name=f"search_agent_{request_id}",
        system_message=search_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    search_agent.register_for_llm(
        name="generate_search_results",
        description="Generates search results for the user query."
    )(generate_search_results)

    # Product selection agent
    product_selection_agent = ConversableAgent(
        name=f"product_selection_agent_{request_id}",
        system_message=product_selection_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    product_selection_agent.register_for_llm(
        name="extract_all_links",
        description="Extracts product links from the search results."
    )(extract_all_links)

    # Data extraction agent
    data_extract_agent = ConversableAgent(
        name=f"data_extract_agent_{request_id}",
        system_message=data_extract_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    data_extract_agent.register_for_llm(
        name="process_links",
        description="Extracts structured data from product links."
    )(process_links)

    # Data frame creator agent
    data_frame_creator_agent = ConversableAgent(
        name=f"data_frame_creator_agent_{request_id}",
        system_message=data_frame_creator_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    data_frame_creator_agent.register_for_llm(
        name="json_to_csv",
        description="Creates a CSV file from the extracted data."
    )(json_to_csv)

    # Entrypoint agent coordinates sub-agents
    result = entrypoint_agent.initiate_chats([
        {
            "recipient": search_agent,
            "message": f"Please execute the `generate_search_results` function. The user query is: {user_query}. Domains to prioritize: {custom_domains}. Tags are: {tags}. country code is : {country_code}. Request ID: {request_id}",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": product_selection_agent,
            "message": f"Please execute the `extract_all_links` function. product or item name is {user_query}. country code is {country_code}. location is {location}. Request ID: {request_id}",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": data_extract_agent,
            "message": f"Please execute the `process_links` function. country code is {country_code}. Request ID: {request_id}", 
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": data_frame_creator_agent,
            "message": f"Please execute the `json_to_csv` function. product or item name is {user_query}. country code is {country_code}. Request ID: {request_id}",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
    ])

    return result

# result = main("White Sauce",None,["white","Sauce","Quality"],"CA","1234567890")