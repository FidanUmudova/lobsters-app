/**
 * ============================================================
 * FRONTEND LOGIC — app.js
 * ============================================================
 * Role: Frontend Developer
 *
 * Responsibility: Fetch the top posts from the Backend API and
 * render them into the page.
 * ============================================================
 */

const API_BASE_URL = "http://localhost:5000";

const postListEl = document.getElementById("post-list");
const stateMessageEl = document.getElementById("state-message");

function formatDate(unixSeconds) {
  const date = new Date(unixSeconds * 1000);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric"
  });
}

function setStateMessage(text, isError = false) {
  stateMessageEl.textContent = text;

  if (isError) {
    stateMessageEl.classList.add("error");
  } else {
    stateMessageEl.classList.remove("error");
  }

  if (text === "") {
    stateMessageEl.style.display = "none";
  } else {
    stateMessageEl.style.display = "";
  }
}

function buildPostHTML(post, rank) {
  return `
    <li class="post-item">
      <div class="post-rank">${rank}</div>
      <div class="post-body">
        <a class="post-title" href="${post.url}" target="_blank" rel="noopener">
          ${post.title}
        </a>
        <div class="post-meta">
          <span>${post.score} points</span>
          <span>by ${post.author}</span>
          <span>${formatDate(post.created_utc)}</span>
          <a href="${post.permalink}" target="_blank" rel="noopener">
            ${post.num_comments} comments
          </a>
        </div>
      </div>
    </li>
  `;
}

function renderPosts(posts) {
  if (posts.length === 0) {
    setStateMessage("No posts found. Has the pipeline been run yet?");
    postListEl.innerHTML = "";
    return;
  }

  setStateMessage("");

  const html = posts
    .map((post, index) => buildPostHTML(post, index + 1))
    .join("");

  postListEl.innerHTML = html;
}

async function fetchTopPosts() {
  setStateMessage("Loading posts...");

  try {
    const response = await fetch(`${API_BASE_URL}/api/posts/top?limit=10`);

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const result = await response.json();

    if (result.success) {
      renderPosts(result.data);
    } else {
      setStateMessage(result.error || "Something went wrong.", true);
    }
  } catch (error) {
    console.error(error);
    setStateMessage(
      "Could not reach the API. Is the backend server running on port 5000?",
      true
    );
  }
}

fetchTopPosts();