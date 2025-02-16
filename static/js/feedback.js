document.getElementById("feedbackForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const responseMessage = document.getElementById("responseMessage");

    if (name === "" || email === "" || message === "") {
        responseMessage.style.color = "red";
        responseMessage.textContent = "Please fill out all fields.";
        return;
    }

    // Simulate feedback submission
    responseMessage.style.color = "#0f0";
    responseMessage.textContent = "Thank you for your feedback!";
    
    // Clear input fields
    document.getElementById("feedbackForm").reset();
});
