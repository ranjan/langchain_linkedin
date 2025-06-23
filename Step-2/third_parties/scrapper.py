import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def scrape_profile(profile_username: str, mock: bool = True, source: str = "LinkedIn"):
    if mock:
        print(f"Using mock results for {source}\n")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        source = source.lower().replace(" ", "_")
        file_map = {
            "linkedin_finder": "linkedin_profile.json",
            "twitter_finder": "twitter_profile.json",
            "github_finder": "github_profile.json",
        }

        mock_filename = file_map.get(source, "linkedin_profile.json")  # fallback
        mock_file = os.path.join(base_dir, "mock_data", mock_filename)

        with open(mock_file, "r") as f:
            response_data = json.load(f)
    else:
        # Live request (not mock)
        # This part is up to your API structure
        raise NotImplementedError("Live scrape not supported yet.")

    person_data = response_data.get("person")
    if not person_data:
        raise ValueError("Missing 'person' key in response.")

    cleaned_data = {
        k: v for k, v in person_data.items()
        if v not in ([], "", None) and k.lower() != "certifications"
    }

    return cleaned_data
