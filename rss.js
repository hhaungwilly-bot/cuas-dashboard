const container = document.getElementById('rss-container');

async function fetchRSSPosts() {
    try {
        const response = await fetch('rss_posts.json');
        const posts = await response.json();

        container.innerHTML = "";

        posts.slice(0,10).forEach(post => {
            const div = document.createElement('div');
            div.className = 'post';
            div.innerHTML = `
                <h4>${post.title}</h4>
                <p>${post.description}</p>
                <a href="${post.link}" target="_blank">Read More</a>
                <small>${new Date(post.pubDate).toLocaleString()}</small>
            `;
            container.appendChild(div);
        });
    } catch (err) {
        container.innerHTML = `<p>Error loading posts: ${err.message}</p>`;
    }
}

fetchRSSPosts();
