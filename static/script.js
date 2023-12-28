async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatbox = document.getElementById('chatbox');
    const message = userInput.value;
    userInput.value = '';

    chatbox.innerHTML += `<div class="message user-message">${message}</div>`;

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();
    chatbox.innerHTML += `<div class="message bot-message">${data.response}</div>`;
}
