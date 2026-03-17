async function loadNews() {
    const res = await fetch('data/news.json');
    const data = await res.json();

    document.getElementById("last-updated").innerText =
        "Last Updated: " + data.last_updated;

    const container = document.getElementById("news-container");

    data.articles.forEach(article => {
        const div = document.createElement("div");
        div.className = "article";

        div.innerHTML = `
            <h3><a href="${article.link}" target="_blank">${article.title}</a></h3>
            <p>${article.source}</p>
            <small>${article.published}</small>
        `;

        container.appendChild(div);
    });
}

loadNews();
