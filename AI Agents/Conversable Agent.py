from collections import defaultdict
from typing import Dict, List
from autogen import ConversableAgent
from math import sqrt
import sys
import os
from dotenv import load_dotenv

load_dotenv()

REVIEWS = defaultdict(list)
with open("restaurant-data.txt") as f:
    for line in f:
        parts = line.split(". ", maxsplit=1)
        if len(parts) == 2:
            name, review = parts
            REVIEWS[name].append(review)

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    return {
        restaurant_name: REVIEWS.get(restaurant_name, [])
    }

def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    # This function takes in a restaurant name, a list of food scores from 1-5, and a list of customer service scores from 1-5
    # The output should be a score between 0 and 10, which is computed as the following:
    # SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    # The above formula is a geometric mean of the scores, which penalizes food quality more than customer service. 
    # Example:
    # > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    # {"Applebee's": 5.048}
    # NOTE: be sure to that the score includes AT LEAST 3  decimal places. The public tests will only read scores that have 
    # at least 3 decimal places.
    denominator = (min(len(food_scores), len(customer_service_scores)) * sqrt(125))
    return {restaurant_name: sum(
            sqrt(food_score**2 * customer_service_score) / denominator
            for food_score, customer_service_score in zip(food_scores, customer_service_scores)
        ) * 10
    }


entrypoint_agent_system_message = f"""
You are responsible for orchestrating the following agents to generate a restaurant summary based on user queries:

- data fetch agent
- review analysis agent
- score agent

For a user query about a restaurant, follow these steps:

1. Send the user query to the data fetch agent.
2. The data fetch agent fetches reviews for the restaurant.
3. Forward the reviews to the review analysis agent to compute numeric scores for each review.
4. Forward these scores to the score agent to calculate the restaurant's overall rating.
5. Provide a brief review summary and return the overall score (rounded to three decimal places).

If an error occurs, stop and display an error message.
"""


data_fetch_agent_system_message = (
    "You are in charge of fetching restaurant review data using a function called "
    "fetch_restaurant_data.\n\n"
    "You will be given a user query about a restaurant, determine which specific "
    "restaurant the query relates to from the following list:\n\n"
    f"{chr(10).join(f'- {key}' for key in REVIEWS.keys())}\n\n"
    "If the user has misspelled the restaurant name, please use the "
    "spelling from the list. For example, if the user asks about 'Applebees', "
    "please call the function with 'Applebee's'. If the user asks about 'InNOut', "
    "'In and Out' or 'In-N-Out', use 'In-n-Out'. If the user asks about an unknown "
    "restaurant, please reply by saying we have no data for that restaurant.\n\n"
    "Invoke the fetch_restaurant_data function which will return reviews for the "
    "restaurant. Return the reviews, one per line."
)

review_analysis_agent_system_message = """
Given a list of restaurant reviews, assess each review and generate two numeric ratings from 1 to 5 for the following:

1. Food quality
2. Customer service

These ratings are determined based on specific keywords in the review text:

1 = {awful, horrible, disgusting}
2 = {bad, unpleasant, offensive}
3 = {average, uninspiring, forgettable}
4 = {good, enjoyable, satisfying}
5 = {awesome, incredible, amazing}

Return two scores separated by a comma, for each review in the same order as
the reviews.
"""

score_agent_system_message = """
You are responsible for calculating a restaurant's overall rating. When provided with the restaurant name and lists of food and customer service ratings, 
invoke the calculate_overall_score function, passing the name, food scores, and customer scores.

Return the result rounded to three decimal places, e.g., 6.254.
"""

# Do not modify the signature of the "main" function.
def main(user_query: str):

    # example LLM config for the entrypoint agent
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]}

    # the main entrypoint/supervisor agent
    entrypoint_agent = ConversableAgent(
        name="entrypoint_agent",
        system_message=entrypoint_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)

    data_fetch_agent = ConversableAgent(
        name="data_fetch_agent",
        system_message=data_fetch_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    data_fetch_agent.register_for_llm(name="fetch_restaurant_data", description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
 
    review_analysis_agent = ConversableAgent(
        name="review_analysis_agent",
        system_message=review_analysis_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )

    score_agent = ConversableAgent(
        name="score_agent",
        system_message=score_agent_system_message,
        llm_config=llm_config,
        human_input_mode='NEVER',
    )
    score_agent.register_for_llm(name="calculate_overall_score", description="Calculates the overall score for a restaurant.")(calculate_overall_score)
    
    result = entrypoint_agent.initiate_chats([
        {
            "recipient": data_fetch_agent,
            "message": f"The user query is: {user_query}",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": review_analysis_agent,
            "message": "Please analyze the reviews and provide scores.",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": score_agent,
            "message": "Please calculate the overall score for the restaurant.",
            "max_turns": 2,
            "summary_method": "last_msg",
        },   
    ])


# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])