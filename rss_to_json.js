const Parser = require('rss-parser');
const fs = require('fs');

const parser = new Parser();
const feeds = [
    'https://news.google.com/rss/search?q=counter+uas+OR+counter+drone',
    'https://dronedj.com/feed/'
];

(async () => {
    try {
        let allPosts = [];
        for (const feedUrl of feeds) {
            const feed = await parser.parseURL(feedUrl);
            const items = feed.items.map(item => ({
                title: item.title,
                link: item.link,
                pubDate: item.pubDate,
                description: item.contentSnippet
            }));
            allPosts = allPosts.concat(items);
        }

        allPosts.sort((a,b) => new Date(b.pubDate) - new Date(a.pubDate));

        fs.writeFileSync('rss_posts.json', JSON.stringify(allPosts, null, 2));
        console.log('rss_posts.json generated!');
    } catch (err) {
        console.error('Error fetching RSS:', err);
    }
})();
