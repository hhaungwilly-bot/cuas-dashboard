import json
from datetime import datetime

# ⚠️ This uses a mock approach (replace with API like Apify or PhantomBuster)
# You can plug real LinkedIn scraping here

companies = [
    {"name": "DroneShield", "category": "AI"},
    {"name": "Sentrycs", "category": "RF"},
    {"name": "SKYLOCK", "category": "Radar"}
]

posts = []

for c in companies:
    posts.append({
        "company": c["name"],
        "text": f"Latest update from {c['name']} (auto-fetched)",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "category": c["category"],
        "link": "https://linkedin.com/"
    })

with open("data/cuas-feed.json", "w") as f:
    json.dump({"posts": posts}, f, indent=2)
