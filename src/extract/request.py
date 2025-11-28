import pandas as pd
import requests

def get_wikipedia_image(name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ', '_')}"
    
    headers = {
        "User-Agent": "BoxingETL/1.0 (mailto:gurvirsingdhillon@outlook.com)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for {name}")
        return None

    data = response.json()

    if "thumbnail" in data:
        return data["thumbnail"]["source"]
    else:
        return None


# Example
fighter_name = "Tyson Fury"
print(get_wikipedia_image(fighter_name))