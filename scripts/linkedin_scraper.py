"""Fetch recent CUAS-related LinkedIn company posts and write dashboard feed JSON.

Usage:
  APIFY_TOKEN=... python scripts/linkedin_scraper.py
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any

import requests

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
OUTPUT_PATH = "data/cuas-feed.json"
MAX_POSTS_PER_COMPANY = int(os.getenv("MAX_POSTS_PER_COMPANY", "8"))

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


def _safe_date(raw_value: Any) -> str:
    if isinstance(raw_value, str) and raw_value:
        return raw_value[:10]

    if isinstance(raw_value, (int, float)):
        return datetime.fromtimestamp(raw_value / 1000, tz=UTC).strftime("%Y-%m-%d")

    return datetime.now(UTC).strftime("%Y-%m-%d")


def normalize_item(item: dict[str, Any]) -> dict[str, str]:
    text = (
        item.get("text")
        or item.get("commentaryText")
        or item.get("postText")
        or ""
    ).strip()

    company = item.get("companyName") or item.get("company") or "Unknown"
    posted_at = item.get("postedAt") or item.get("postedAtTimestamp")

    return {
        "company": str(company),
        "text": text[:280],
        "date": _safe_date(posted_at),
        "category": detect_category(text),
        "link": item.get("url") or item.get("postUrl") or "https://linkedin.com",
    }


def fetch_posts() -> list[dict[str, str]]:
    if not APIFY_TOKEN:
        raise RuntimeError("APIFY_TOKEN is required to fetch LinkedIn data.")

    payload = {
        "companyUrls": COMPANY_URLS,
        "maxPosts": MAX_POSTS_PER_COMPANY,
    }
    response = requests.post(
        APIFY_ACTOR_URL,
        params={"token": APIFY_TOKEN},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()

    raw_items = response.json()
    posts = [normalize_item(item) for item in raw_items]
    posts = [post for post in posts if post["text"]]
    posts.sort(key=lambda post: post["date"], reverse=True)
    return posts


def main() -> None:
    posts = fetch_posts()
    output = {
        "updatedAt": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "LinkedIn company pages via Apify actor",
        "postCount": len(posts),
        "posts": posts,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print(f"Wrote {len(posts)} posts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
