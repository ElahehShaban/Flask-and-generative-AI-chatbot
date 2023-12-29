async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatbox = document.getElementById('chatbox');
    const message = userInput.value.trim();
    userInput.value = '';

    if (message) {
        const messageHTML = `<div class="message-pair">
                                <div class="message user-message">${message}</div>`;
        chatbox.innerHTML += messageHTML;
        chatbox.scrollTop = chatbox.scrollHeight;

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        chatbox.innerHTML += `<div class="message bot-message">${data.response}</div></div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}
