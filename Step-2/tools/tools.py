from langchain_community.tools.tavily_search import TavilySearchResults
import json

from dotenv import load_dotenv
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

USE_MOCK = True
def get_profile_url_tavily(name: str):
    if USE_MOCK:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mock_file = os.path.join(base_dir, "mock_data", "linkedin_results.json")
        with open(mock_file, "r") as f:
            mock_results = json.load(f)
        print("Using mock Linkedin Tavily results\n")
        print(mock_results)
        return mock_results[0]["url"] if mock_results else None
    else:
        from langchain_community.tools.tavily_search import TavilySearchResults
        search = TavilySearchResults()
        res = search.run(f"{name}")
        print("Live Linkedin Tavily Results... \n")
        print(res)
        return res[0]["url"] if res else None

def get_twitter_profile(name: str):
    if USE_MOCK:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mock_file = os.path.join(base_dir, "mock_data", "twitter_results.json")
        with open(mock_file, "r") as f:
            mock_results = json.load(f)
        print("Using mock Twitter results\n")
        print(mock_results)
        return mock_results[1]["url"] if mock_results else None
    else:
        # Normally you'd call Twitter/X API here
        print("Live Twitter lookup not implemented")
        return None

def get_github_profile(name: str):
    if USE_MOCK:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mock_file = os.path.join(base_dir, "mock_data", "github_results.json")
        with open(mock_file, "r") as f:
            mock_results = json.load(f)
        print("Using mock GitHub results\n")
        print(mock_results)
        return mock_results[4]["url"] if mock_results else None
    else:
        # Normally you'd call GitHub API here
        print("Live GitHub lookup not implemented")
        return None

