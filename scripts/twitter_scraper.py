"""Fetch recent CUAS-related Twitter/X posts and write dashboard feed JSON.

Usage:
  TWITTER_BEARER_TOKEN=... python scripts/twitter_scraper.py
"""

import json
import os
from datetime import datetime, timezone
from urllib.parse import quote_plus

import requests

OUTPUT_PATH = "data/cuas-feed.json"
MAX_RESULTS = 100

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

# Focused query for C-UAS / counter-drone intelligence from key vendor accounts + topic terms.
QUERY = (
    "(cuas OR \"counter uas\" OR \"counter-uas\" OR \"counter drone\" OR \"counter-drone\" "
    "OR anti-drone OR \"unmanned aerial\" OR uas OR uav OR drone) "
    "(from:DroneShieldLtd OR from:Dedrone OR from:Sentrycs OR from:FortemTech OR from:RobinRadar) "
    "-is:retweet -is:reply lang:en"
)


def detect_category(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ("jam", "rf", "electronic warfare", "spoof")):
        return "RF"
    if any(word in lowered for word in ("ai", "autonomy", "machine learning", "classifier")):
        return "AI"
    if any(word in lowered for word in ("radar", "sensor", "detection", "tracking")):
        return "Radar"
    if any(word in lowered for word in ("interceptor", "kinetic", "mitigation", "neutralize")):
        return "Mitigation"
    return "General"


def fetch_tweets() -> list[dict]:
    if not TWITTER_BEARER_TOKEN:
        raise RuntimeError("TWITTER_BEARER_TOKEN is required to fetch Twitter/X data.")

    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {
        "query": QUERY,
        "max_results": MAX_RESULTS,
        "expansions": "author_id",
        "tweet.fields": "created_at,text,author_id",
        "user.fields": "name,username",
    }

    response = requests.get(TWITTER_SEARCH_URL, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()

    users = {user["id"]: user for user in payload.get("includes", {}).get("users", [])}
    posts = []

    for tweet in payload.get("data", []):
        text = tweet.get("text", "").strip()
        if not text:
            continue

        author = users.get(tweet.get("author_id"), {})
        username = author.get("username", "unknown")
        created_at = tweet.get("created_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

        posts.append(
            {
                "company": author.get("name", f"@{username}"),
                "text": text[:280],
                "date": created_at[:10],
                "category": detect_category(text),
                "link": f"https://x.com/{username}/status/{tweet.get('id')}",
            }
        )

    posts.sort(key=lambda post: post["date"], reverse=True)
    return posts


def main() -> None:
    posts = fetch_tweets()
    output = {
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": f"Twitter/X recent search: {quote_plus(QUERY)}",
        "posts": posts,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Wrote {len(posts)} posts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
