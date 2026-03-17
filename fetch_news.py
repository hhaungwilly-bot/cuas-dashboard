import feedparser
import json
from datetime import datetime

# Google News RSS for Counter-UAS
RSS_URL = "https://news.google.com/rss/search?q=counter+UAS+drone+defense&hl=en-US&gl=US&ceid=US:en"

feed = feedparser.parse(RSS_URL)

articles = []

for entry in feed.entries[:20]:
    articles.append({
        "title": entry.title,
        "link": entry.link,
        "published": entry.published,
        "source": entry.source.title if "source" in entry else "Unknown"
    })

output = {
    "last_updated": datetime.utcnow().isoformat(),
    "articles": articles
}

with open("data/news.json", "w") as f:
    json.dump(output, f, indent=2)

print("News updated!")
