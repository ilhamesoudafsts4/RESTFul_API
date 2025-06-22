async function fetchComments() {
  const subfeddit = document.getElementById("subfedditInput").value.trim();
  const start = document.getElementById("startInput").value;
  const end = document.getElementById("endInput").value;
  const sortByPolarity = document.getElementById("sortCheckbox").checked;
  const container = document.getElementById("commentsContainer");
  container.innerHTML = "";

  if (!subfeddit) {
    container.innerHTML = "<p class='error'>Please enter a subfeddit name.</p>";
    return;
  }

  let url = `/comments?subfeddit=${encodeURIComponent(subfeddit)}`;
  if (start) url += `&start=${encodeURIComponent(start)}`;
  if (end) url += `&end=${encodeURIComponent(end)}`;
  if (sortByPolarity) url += `&sort_by_polarity=true`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = "<p class='empty'>No comments found for this subfeddit.</p>";
      return;
    }

    data.forEach(comment => {
      const div = document.createElement("div");
      div.className = "comment";

      div.innerHTML = `
        <div class="meta">Comment ID: <strong>${comment.id}</strong> | Date: ${comment.created_at}</div>
        <div class="text">${comment.text}</div>
        <div>Polarity: ${comment.polarity.toFixed(2)} — 
          <span class="${comment.sentiment}">${comment.sentiment.toUpperCase()}</span>
        </div>
      `;

      container.appendChild(div);
    });
  } catch (err) {
    console.error(err);
    container.innerHTML = "<p class='error'>Failed to fetch comments. Please try again.</p>";
  }
}
