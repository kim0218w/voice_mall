document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  let lastMessageIndex = 0;

  const scrollToBottom = () => {
    chatBox.scrollTop = chatBox.scrollHeight;
  };

  const loadMessages = () => {
    fetch("chat.json")
      .then((response) => response.json())
      .then((data) => {
        const messages = data.messages;

        // 새로운 메시지를 채팅 박스에 추가
        for (let i = lastMessageIndex; i < messages.length; i++) {
          const message = messages[i];
          const messageElement = document.createElement("div");
          messageElement.classList.add("message", message.sender);

          const profilePicElement = document.createElement("img");
          profilePicElement.classList.add("profile-pic");

          // 발신자에 따라 프로필 사진 설정
          if (message.sender === "ai") {
            profilePicElement.src = "./ai_광태.png"; // AI 프로필 사진 경로
          } else if (message.sender === "client") {
            profilePicElement.src = "human_profile.png"; // 클라이언트 프로필 사진 경로
          } else {
            profilePicElement.src = "default-profile-pic.png"; // 기본 프로필 사진 경로
          }

          const bubbleElement = document.createElement("div");
          bubbleElement.classList.add("bubble");

          // 메시지 내용이 이미지 파일인지 확인
          if (/\.(jpeg|jpg|gif|png)$/.test(message.text)) {
            const imageElement = document.createElement("img");
            imageElement.src = message.text;
            imageElement.style.maxWidth = "100%";
            bubbleElement.appendChild(imageElement);

            // 이미지 로드 완료 후 채팅 박스를 아래로 스크롤
            imageElement.onload = scrollToBottom;
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
        }

        // 마지막 메시지 인덱스 업데이트
        lastMessageIndex = messages.length;
      })
      .catch((error) => console.error("채팅 데이터 로드 오류:", error));
  };

  // 초기 로드
  loadMessages();

  // 새로운 메시지를 1초마다 확인
  setInterval(loadMessages, 1000);
});
