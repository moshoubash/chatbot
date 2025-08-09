async function sendMessage() {
    let input = document.getElementById("user-input");
    let sendButton = document.getElementById("send-button");
    let message = input.value.trim();
    if (!message) return;

    // Disable send button and show spinner
    sendButton.disabled = true;
    sendButton.innerHTML = '<span class="spinner"></span>';

    // Hide header when first message is sent
    let header = document.getElementById("header");
    header.style.display = "none";

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class='user-msg'>${message}</div>`;

    try {
        let res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                'message': message
            })
        });
        let data = await res.json();

        chatBox.innerHTML += `<div class='bot-msg'>${data.response || data.error}</div>`;
        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        chatBox.innerHTML += `<div class='bot-msg'>Error: Failed to send message</div>`;
    } finally {
        sendButton.disabled = false;
        sendButton.innerHTML = 'Send';
    }
}
