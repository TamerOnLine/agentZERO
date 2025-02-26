import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from serpapi import GoogleSearch
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationSummaryBufferMemory

# Load environment variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

if not SERPAPI_KEY:
    print("Warning: SERPAPI_KEY not found, search may not work correctly.")


def search_google(query, site):
    """Search a specific site using Google through SerpAPI."""
    if not SERPAPI_KEY:
        print("Warning: Missing API key, search will not work.")
        return []
    
    search_query = f"{query} site:{site}"
    params = {
        "q": search_query,
        "api_key": SERPAPI_KEY
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("organic_results", [])
    except Exception as e:
        print(f"Search error: {e}")
        return []


def scrape_page(url, text_limit=1000):
    """Extract text from a web page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().strip()
        return text[:text_limit] if len(text) > text_limit else text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Configure Ollama LLM
llm = OllamaLLM(
    model="llama3",
    system_message="Analyze the text and provide a clear summary in valid JSON format.",
    output_format="json",
    strict_mode=True,
    low_cpu_mem_usage=True
)

# Configure tools
target_site = "https://clinicaltrials.gov/"

tools = [
    Tool(
        name="Google Search",
        func=lambda query: search_google(query, target_site),
        description="Search within clinicaltrials.gov only."
    ),
    Tool(
        name="Web Scraper",
        func=scrape_page,
        description="Extract text from a web page."
    )
]

# Create conversation memory
memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    max_iterations=3
)

# Execute search
query = "Blood pressure symptoms"
print(f"Searching for: {query} on {target_site}...")

try:
    search_results = agent.invoke(query)
    
    if isinstance(search_results, list) and search_results:
        first_result_url = search_results[0].get("link", "")
        if first_result_url:
            print(f"Extracted URL: {first_result_url}")
            scraped_content = scrape_page(first_result_url, text_limit=500)
            
            if scraped_content:
                try:
                    response = llm.invoke(scraped_content)
                    print("Ollama Analysis:")
                    print(response)
                except Exception as e:
                    print(f"Error processing content with Ollama: {e}")
            else:
                print("No content extracted from the page.")
        else:
            print("No link found in search results.")
    else:
        print("No search results found.")
except Exception as e:
    print(f"Error executing search: {e}")