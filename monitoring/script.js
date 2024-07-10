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

          const profilePicElement = document.createElement("img");
          profilePicElement.classList.add("profile-pic");

          // Set profile picture based on sender
          if (message.sender === "ai") {
            profilePicElement.src = "./ai_광태.png"; // Path to AI profile picture
          } else if (message.sender === "client") {
            profilePicElement.src = "human_profile.png"; // Path to client profile picture
          } else {
            profilePicElement.src = "default-profile-pic.png"; // Default profile picture
          }

          const bubbleElement = document.createElement("div");
          bubbleElement.classList.add("bubble");

          // Check if the message text is a URL to an image
          if (/\.(jpeg|jpg|gif|png)$/.test(message.text)) {
            const imageElement = document.createElement("img");
            imageElement.src = message.text;
            imageElement.style.maxWidth = "100%";
            bubbleElement.appendChild(imageElement);
          } else {
            const textElement = document.createElement("p");
            textElement.textContent = message.text;
            bubbleElement.appendChild(textElement);
          }

          if (message.sender === "client") {
            messageElement.appendChild(bubbleElement);
            messageElement.appendChild(profilePicElement);
          } else {
            messageElement.appendChild(profilePicElement);
            messageElement.appendChild(bubbleElement);
          }
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
