// Get recommended games from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const games = JSON.parse(urlParams.get("games") || "[]"); // Parse as JSON array

// Reference to the game list
const gameList = document.getElementById("gameList");

// Append each game with a like button
games.forEach(game => {
    let li = document.createElement("li");
    li.innerHTML = `
        <span>${game}</span>
        <button class="like-btn" onclick="likeGame(this)">💙</button>
    `;
    gameList.appendChild(li);
});

function likeGame(button) {
    button.textContent = "💜";
    button.style.backgroundColor = "#ff0";
    button.style.color = "#000";
    button.disabled = true;
}