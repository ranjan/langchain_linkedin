import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:

        #linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/32f3c85b9513994c572613f2c8b376b633bfc43f/eden-marco-scrapin.json"
        # response_data = requests.get(
        #     linkedin_profile_url,
        #     timeout=10,
        # )
        print("Using mock Linkedin results\n")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mock_file = os.path.join(base_dir, "mock_data", "linkedin_profile.json")

        with open(mock_file, "r") as f:
            response_data = json.load(f)  # Already a dict
    else:
        print("Using Live Linkedin results\n")
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)
        response_data = response.json()  # Turn response into dict

    # Now `response_data` is always a dict
    data = response_data.get("person")

    if not data:
        raise ValueError("Missing 'person' key in response data.")

    # Clean the data
    cleaned_data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k.lower() != "certifications"
    }

    return cleaned_data
