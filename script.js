
let allPosts = [];

async function loadData() {
  const res = await fetch('data/cuas-feed.json');
  const data = await res.json();
  allPosts = data.posts;
  renderPosts(allPosts);
}

function renderPosts(posts) {
  const container = document.getElementById('feed');
  container.innerHTML = '';

  posts.forEach(post => {
    const div = document.createElement('div');
    div.className = 'card';

    div.innerHTML = `
      <h2>${post.company}</h2>
      <p>${post.text}</p>
      <small>${post.date} | ${post.category}</small>
      <br><a href="${post.link}" target="_blank">View Post</a>
    `;

    container.appendChild(div);
  });
}

function filterPosts(category) {
  if (category === 'all') {
    renderPosts(allPosts);
  } else {
    const filtered = allPosts.filter(p => p.category === category);
    renderPosts(filtered);
  }
}

loadData();

