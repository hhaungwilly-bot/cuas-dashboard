const container = document.getElementById('linkedin-container');

async function fetchLinkedInPosts() {
  try {
    const response = await fetch('linkedin_posts.json');
    const posts = await response.json();

    container.innerHTML = "";

    posts.forEach(post => {
      const div = document.createElement('div');
      div.className = 'post';
      div.innerHTML = `
        <h4>${post.author}</h4>
        <p>${post.content}</p>
        <a href="${post.postUrl}" target="_blank">View Post</a>
        <small>${new Date(post.createdAt).toLocaleString()}</small>
      `;
      container.appendChild(div);
    });

  } catch (err) {
    container.innerHTML = `<p>Error loading LinkedIn posts: ${err.message}</p>`;
  }
}

fetchLinkedInPosts();
