// static/script.js

document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const inputField = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-btn");

    // Function to append messages to chat
    function appendMessage(sender, message) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", sender);

        msgDiv.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Handle sending messages
    async function sendMessage() {
        const userMessage = inputField.value.trim();
        if (!userMessage) return;

        appendMessage("user", userMessage);
        inputField.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            appendMessage("bot", data.reply || "⚠️ No response from server.");
        } catch (error) {
            appendMessage("bot", "❌ Error connecting to server.");
            console.error("Error:", error);
        }
    }

    // Event listeners
    sendButton.addEventListener("click", sendMessage);
    inputField.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});
