document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  let lastMessageIndex = 0;

  const loadMessages = () => {
    fetch("chat.json")
      .then((response) => response.json())
      .then((data) => {
        const messages = data.messages;

        // Add new messages to the chat box
        for (let i = lastMessageIndex; i < messages.length; i++) {
          const message = messages[i];
          const messageElement = document.createElement("div");
          messageElement.classList.add("message", message.sender);

          const bubbleElement = document.createElement("div");
          bubbleElement.classList.add("bubble");

          const textElement = document.createElement("p");
          textElement.textContent = message.text;

          bubbleElement.appendChild(textElement);
          messageElement.appendChild(bubbleElement);
          chatBox.appendChild(messageElement);

          // Scroll to the bottom of the chat box
          chatBox.scrollTop = chatBox.scrollHeight;
        }

        // Update the last message index
        lastMessageIndex = messages.length;
      })
      .catch((error) => console.error("Error fetching chat data:", error));
  };

  // Initial load
  loadMessages();

  // Poll for new messages every 1 seconds
  setInterval(loadMessages, 1000);
});
