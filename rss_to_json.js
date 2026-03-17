const fs = require('fs/promises');

const FEEDS = [
  {
    source: 'Google News: counter UAS',
    url: 'https://news.google.com/rss/search?q=%22counter+UAS%22+OR+%22counter-drone%22&hl=en-US&gl=US&ceid=US:en'
  },
  {
    source: 'Google News: drone defense',
    url: 'https://news.google.com/rss/search?q=%22drone+defense%22+OR+%22anti-drone%22&hl=en-US&gl=US&ceid=US:en'
  }
];

function decodeXml(text = '') {
  return text
    .replace(/<!\[CDATA\[(.*?)\]\]>/gs, '$1')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/<[^>]*>/g, '')
    .trim();
}

function extractTagValue(xmlChunk, tagName) {
  const match = xmlChunk.match(new RegExp(`<${tagName}[^>]*>([\\s\\S]*?)<\\/${tagName}>`, 'i'));
  return match ? decodeXml(match[1]) : '';
}

function parseRssItems(xmlText, source) {
  const itemMatches = xmlText.match(/<item[\s\S]*?<\/item>/gi) || [];

  return itemMatches
    .map((itemXml) => ({
      title: extractTagValue(itemXml, 'title') || 'Untitled article',
      description: extractTagValue(itemXml, 'description'),
      link: extractTagValue(itemXml, 'link'),
      pubDate: extractTagValue(itemXml, 'pubDate') || new Date().toISOString(),
      source
    }))
    .filter((item) => item.link);
}

async function fetchFeed(feed) {
  try {
    const response = await fetch(feed.url, {
      headers: {
        'User-Agent': 'cuas-dashboard-rss-fetcher/1.0'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const xmlText = await response.text();
    return parseRssItems(xmlText, feed.source);
  } catch (error) {
    const causeMessage = error.cause && error.cause.message ? ` (cause: ${error.cause.message})` : '';
    console.error(`Failed to fetch ${feed.source}: ${error.message}${causeMessage}`);
    return [];
  }
}

function getNetworkHint() {
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy || process.env.HTTP_PROXY || process.env.http_proxy;

  if (!proxy) {
    return 'No proxy configured. Verify this runtime can reach the public internet.';
  }

  return `Proxy detected (${proxy}). If requests fail with CONNECT 403 or "fetch failed", the proxy policy is blocking outbound RSS domains.`;
}

async function buildRssJson() {
  const itemsByFeed = await Promise.all(FEEDS.map(fetchFeed));

  const posts = Array.from(
    new Map(itemsByFeed.flat().map((item) => [item.link, item])).values()
  )
    .sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate))
    .slice(0, 50);

  if (!posts.length) {
    try {
      await fs.access('rss_posts.json');
      console.log('No fresh RSS items fetched. Keeping existing rss_posts.json.');
      console.log(getNetworkHint());
      return;
    } catch {
      console.log('No RSS items fetched and no existing cache found. Writing placeholder news item.');
      posts.push({
        title: 'RSS feed temporarily unavailable',
        description: 'The dashboard could not fetch remote RSS feeds during this build. This usually means outbound traffic to the RSS host is blocked by network policy/proxy.',
        link: '#',
        pubDate: new Date().toISOString(),
        source: 'Build status'
      });
      console.log(getNetworkHint());
    }
  }

  await fs.writeFile('rss_posts.json', JSON.stringify(posts, null, 2));
  console.log(`Saved ${posts.length} RSS posts to rss_posts.json`);
}

buildRssJson().catch((error) => {
  console.error(`Unable to build RSS JSON: ${error.message}`);
  process.exit(1);
});
