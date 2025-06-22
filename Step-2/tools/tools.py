from langchain_community.tools.tavily_search import TavilySearchResults
import json

from dotenv import load_dotenv
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

USE_MOCK = True
def get_profile_url_tavily(name: str):
    if USE_MOCK:
        mock_file = os.path.join(os.path.dirname(__file__), "mock_data", "tavily_results.json")
        with open(mock_file, "r") as f:
            mock_results = json.load(f)
        print("Using mock Tavily results\n")
        return mock_results[0]["url"] if mock_results else None
    else:
        from langchain_community.tools.tavily_search import TavilySearchResults
        search = TavilySearchResults()
        res = search.run(f"{name}")
        print("Live Tavily Results \n")
        return res[0]["url"] if res else None
