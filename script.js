let allPosts = [];
let activeCategory = 'All';
let searchTerm = '';

async function loadData() {
  const res = await fetch('data/cuas-feed.json');
  const data = await res.json();

  allPosts = (data.posts || [])
    .slice()
    .sort((a, b) => new Date(b.date) - new Date(a.date));

  renderMeta();
  renderFilters();
  renderStats();
  renderPosts();
  wireSearch();
}

function renderMeta() {
  const meta = document.getElementById('last-updated');
  const latest = allPosts[0]?.date;
  meta.textContent = latest
    ? `Latest source post date: ${latest}`
    : 'No data available. Run scripts/linkedin_scraper.py to refresh feed.';
}

function renderStats() {
  const stats = document.getElementById('stats');
  const categories = countByCategory(allPosts);

  const blocks = [
    { label: 'Total Posts', value: allPosts.length },
    ...Object.entries(categories).map(([label, value]) => ({ label, value }))
  ];

  stats.innerHTML = blocks
    .map(b => `<div class="stat-card"><div class="label">${b.label}</div><div class="value">${b.value}</div></div>`)
    .join('');
}

function renderFilters() {
  const container = document.getElementById('category-filters');
  const categories = ['All', ...Object.keys(countByCategory(allPosts))];

  container.innerHTML = categories
    .map(c => `<button class="filter-btn ${c === activeCategory ? 'active' : ''}" data-category="${c}">${c}</button>`)
    .join('');

  container.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      activeCategory = btn.dataset.category;
      renderFilters();
      renderPosts();
    });
  });
}

function wireSearch() {
  const search = document.getElementById('search');
  search.addEventListener('input', (e) => {
    searchTerm = e.target.value.trim().toLowerCase();
    renderPosts();
  });
}

function filteredPosts() {
  return allPosts.filter(post => {
    const categoryMatch = activeCategory === 'All' || post.category === activeCategory;
    const term = `${post.company} ${post.text}`.toLowerCase();
    const searchMatch = !searchTerm || term.includes(searchTerm);
    return categoryMatch && searchMatch;
  });
}

function renderPosts() {
  const container = document.getElementById('feed');
  const template = document.getElementById('post-template');
  const posts = filteredPosts();

  container.innerHTML = '';

  if (!posts.length) {
    container.innerHTML = '<div class="empty">No posts match your filters.</div>';
    return;
  }

  posts.forEach(post => {
    const node = template.content.cloneNode(true);
    node.querySelector('h2').textContent = post.company;
    node.querySelector('.category').textContent = post.category;
    node.querySelector('.text').textContent = post.text;
    node.querySelector('.date').textContent = post.date;

    const link = node.querySelector('a');
    link.href = post.link;

    container.appendChild(node);
  });
}

function countByCategory(posts) {
  return posts.reduce((acc, post) => {
    const key = post.category || 'General';
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
}

loadData();
