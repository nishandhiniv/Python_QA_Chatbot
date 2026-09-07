async function sendQuestion() {
    const input = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");

    const question = input.value.trim();

    if (question === "") {
        return;
    }

    // Show user message
    const userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.innerHTML = "<strong>You:</strong> " + question;
    chatBox.appendChild(userMessage);

    input.value = "";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Show bot response
        const botMessage = document.createElement("div");
        botMessage.className = "message bot-message";
        botMessage.innerHTML = "<strong>Bot:</strong> " + data.answer;
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        const errorMessage = document.createElement("div");
        errorMessage.className = "message bot-message";
        errorMessage.innerHTML = "<strong>Bot:</strong> Something went wrong. Please try again.";
        chatBox.appendChild(errorMessage);
    }
}

// Press Enter to send
document.getElementById("question").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendQuestion();
    }
});