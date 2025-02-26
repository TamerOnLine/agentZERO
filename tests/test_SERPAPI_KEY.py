from dotenv import load_dotenv, find_dotenv
import os

# Check if the .env file exists and load it if available
if not find_dotenv():
    print("Warning: .env file not found. Ensure it exists in the correct path.")
else:
    load_dotenv()

# Retrieve the SERPAPI_KEY from environment variables
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    print("Warning: SERPAPI_KEY not found. Google search operations will be disabled.")
else:
    print("SERPAPI_KEY loaded successfully.")

# Prevent execution when imported as a module
if __name__ == "__main__":
    print("SERPAPI_KEY.py executed successfully.")
