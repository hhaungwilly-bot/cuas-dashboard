import json
import os
import requests
from datetime import datetime

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

# Example Apify Actor (LinkedIn company posts scraper)
APIFY_ACTOR_URL = "https://api.apify.com/v2/acts/apify~linkedin-company-posts-scraper/run-sync-get-dataset-items"

params = {
    "token": APIFY_TOKEN
}

payload = {
    "companyUrls": [
        "https://www.linkedin.com/company/droneshield/",
        "https://www.linkedin.com/company/sentrycs/",
        "https://www.linkedin.com/company/skylock/"
    ],
    "maxPosts": 5
}

response = requests.post(APIFY_ACTOR_URL, params=params, json=payload)
data = response.json()

posts = []

for item in data:
    text = item.get("text", "")

    # simple categorization
    if "AI" in text:
        category = "AI"
    elif "RF" in text:
        category = "RF"
    elif "radar" in text.lower():
        category = "Radar"
    else:
        category = "General"

    posts.append({
        "company": item.get("companyName", "Unknown"),
        "text": text[:200],
        "date": item.get("postedAt", datetime.utcnow().strftime("%Y-%m-%d")),
        "category": category,
        "link": item.get("url", "https://linkedin.com")
    })

with open("data/cuas-feed.json", "w") as f:
    json.dump({"posts": posts}, f, indent=2)
