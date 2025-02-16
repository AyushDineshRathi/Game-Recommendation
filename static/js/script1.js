document.getElementById("gameForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    const formData = {
        name: document.getElementById("name").value,
        genres: document.getElementById("genres").value.split(","), // Convert to list
        category: document.getElementById("category").value,
        developers: document.getElementById("developers").value,
        about: document.getElementById("about").value
    };

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.recommendations) {
            const games = encodeURIComponent(JSON.stringify(data.recommendations));

            window.location.href = `/after?games=${games}`;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});