import os
from dotenv import load_dotenv
from langchain_community.tools import Tool
from langchain_community.utilities import SerpAPIWrapper

# Load environment variables from .env
load_dotenv()

# Retrieve API key
serpapi_api_key = os.getenv("SERPAPI_KEY")

# Check if API key exists
if not serpapi_api_key:
    raise ValueError("SERPAPI_KEY not found in .env file")

# Create SerpAPIWrapper with API key
search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

# Define the search tool
search_tool = Tool(
    name="Google Search",
    func=search.run,
    description="Search Google using SerpAPI"
)

# Execute search with error handling
try:
    result = search_tool.run("What are the symptoms of high blood pressure?")
    print(result)
except Exception as e:
    print(f"An error occurred during search execution: {e}")
