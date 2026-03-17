# CUAS Dashboard (GitHub Pages Ready)

A lightweight Counter-Drone (CUAS) intelligence dashboard that displays recent posts pulled from Twitter/X.

## What this includes

- Responsive dashboard UI with:
  - category filters
  - keyword search
  - post feed sorted by recency
  - summary statistic cards
- A Python script to refresh feed data from Twitter/X using the API v2 recent-search endpoint.

## Run locally

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Refresh Twitter/X data

1. Create a Twitter/X developer app with API v2 access and export your bearer token.
2. Run:

```bash
TWITTER_BEARER_TOKEN=your_token_here python scripts/twitter_scraper.py
```

This writes to `data/cuas-feed.json` with real tweet permalinks (`https://x.com/<user>/status/<id>`), which is what GitHub Pages serves.

## Deploy to GitHub Pages

1. Push this repo to GitHub.
2. In repository settings, enable **Pages**.
3. Set source to deploy from your default branch root.
4. Your dashboard will be available at:
   `https://<your-username>.github.io/<repo-name>/`

## Automated refresh (every 30 minutes)

A GitHub Actions workflow runs every 30 minutes and updates `data/cuas-feed.json` automatically.

1. Add a repository secret named `TWITTER_BEARER_TOKEN`.
2. Ensure Actions are enabled for the repository.
3. Optionally run the workflow manually from the Actions tab (`workflow_dispatch`).

