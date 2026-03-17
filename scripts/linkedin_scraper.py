"""Fetch recent CUAS-related LinkedIn company posts and write dashboard feed JSON.

Usage:
  APIFY_TOKEN=... python scripts/linkedin_scraper.py
"""

import json
import os
from datetime import datetime

import requests

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
OUTPUT_PATH = "data/cuas-feed.json"
MAX_POSTS_PER_COMPANY = 8

COMPANY_URLS = [
    "https://www.linkedin.com/company/droneshield/",
    "https://www.linkedin.com/company/sentrycs/",
    "https://www.linkedin.com/company/skylock/",
    "https://www.linkedin.com/company/dedrone/",
    "https://www.linkedin.com/company/fortem-technologies/",
]

APIFY_ACTOR_URL = (
    "https://api.apify.com/v2/acts/"
    "apify~linkedin-company-posts-scraper/run-sync-get-dataset-items"
)


def detect_category(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ("jam", "rf", "electronic warfare")):
        return "RF"
    if any(word in lowered for word in ("ai", "autonomy", "machine learning")):
        return "AI"
    if any(word in lowered for word in ("radar", "rfar", "sensor")):
        return "Radar"
    if any(word in lowered for word in ("interceptor", "kinetic", "mitigation")):
        return "Mitigation"
    return "General"


def normalize_item(item: dict) -> dict:
    text = item.get("text", "").strip()
    return {
        "company": item.get("companyName", "Unknown"),
        "text": text[:280],
        "date": item.get("postedAt", datetime.utcnow().strftime("%Y-%m-%d"))[:10],
        "category": detect_category(text),
        "link": item.get("url", "https://linkedin.com"),
    }


def fetch_posts() -> list[dict]:
    if not APIFY_TOKEN:
        raise RuntimeError("APIFY_TOKEN is required to fetch LinkedIn data.")

    payload = {"companyUrls": COMPANY_URLS, "maxPosts": MAX_POSTS_PER_COMPANY}
    response = requests.post(
        APIFY_ACTOR_URL,
        params={"token": APIFY_TOKEN},
        json=payload,
        timeout=60,
    )

    if response.status_code >= 400:
        message = response.text.strip()[:500]
        raise RuntimeError(
            f"Apify request failed with HTTP {response.status_code}. Response: {message}"
        )

    raw_items = response.json()
    if not isinstance(raw_items, list):
        raise RuntimeError(
            "Unexpected Apify response shape. Expected a list of posts from "
            "run-sync-get-dataset-items."
        )

    posts = [normalize_item(item) for item in raw_items if item.get("text")]
    posts.sort(key=lambda post: post["date"], reverse=True)
    return posts


def main() -> None:
    posts = fetch_posts()
    output = {
        "updatedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "LinkedIn company pages via Apify actor",
        "posts": posts,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Wrote {len(posts)} posts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
