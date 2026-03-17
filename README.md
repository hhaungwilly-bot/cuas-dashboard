# CUAS Dashboard (GitHub Pages Ready)

A lightweight Counter-Drone (CUAS) intelligence dashboard that displays recent posts pulled from LinkedIn company pages.

## What this includes

- Responsive dashboard UI with:
  - category filters
  - keyword search
  - post feed sorted by recency
  - summary statistic cards
- A Python script to refresh feed data from LinkedIn pages using an Apify actor.
- A GitHub Actions workflow that can refresh `data/cuas-feed.json` every hour and commit changes automatically.

## Run locally

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Refresh LinkedIn data manually

1. Create an Apify token and export it.
2. Run:

```bash
APIFY_TOKEN=your_token_here python scripts/linkedin_scraper.py
```

This overwrites `data/cuas-feed.json` with the latest scraper result.

## Enable automatic real-time refresh on GitHub

1. In your GitHub repository, go to **Settings → Secrets and variables → Actions**.
2. Add repository secret `APIFY_TOKEN` with your Apify token value.
3. The workflow `.github/workflows/refresh-linkedin-feed.yml` runs hourly and can also be triggered manually from the **Actions** tab.
4. Each successful run updates and commits `data/cuas-feed.json` when posts change.

## Deploy to GitHub Pages

1. Push this repo to GitHub.
2. In repository settings, enable **Pages**.
3. Set source to deploy from your default branch root.
4. Your dashboard will be available at:
   `https://<your-username>.github.io/<repo-name>/`
