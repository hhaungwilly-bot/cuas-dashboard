const container = document.getElementById('rss-container');

function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value || '';
  return div.innerHTML;
}

async function fetchRSSPosts() {
  try {
    const response = await fetch('rss_posts.json', { cache: 'no-cache' });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const posts = await response.json();

    if (!posts.length) {
      container.innerHTML = '<p>No news articles available right now.</p>';
      return;
    }

    container.innerHTML = '';

    posts.slice(0, 10).forEach((post) => {
      const div = document.createElement('div');
      div.className = 'post';
      div.innerHTML = `
        <h4>${escapeHtml(post.title)}</h4>
        <p>${escapeHtml(post.description || 'No summary available.')}</p>
        <a href="${post.link}" target="_blank" rel="noopener noreferrer">Read More</a>
        <small>${new Date(post.pubDate).toLocaleString()}${post.source ? ` • ${escapeHtml(post.source)}` : ''}</small>
      `;
      container.appendChild(div);
    });
  } catch (err) {
    container.innerHTML = `<p>Error loading posts: ${escapeHtml(err.message)}</p>`;
  }
}

fetchRSSPosts();
