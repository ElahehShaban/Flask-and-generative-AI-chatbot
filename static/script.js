// async function sendMessage() {
//     const userInput = document.getElementById('userInput');
//     const chatbox = document.getElementById('chatbox');
//     const message = userInput.value.trim();
//     userInput.value = '';

//     if (message) {
//         const messageHTML = `<div class="message-pair">
//                                 <div class="message user-message">${message}</div>`;
//         chatbox.innerHTML += messageHTML;
//         chatbox.scrollTop = chatbox.scrollHeight;

//         const response = await fetch('/chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ message: message })
//         });

//         const data = await response.json();
//         chatbox.innerHTML += `<div class="message bot-message">${data.response}</div></div>`;
//         chatbox.scrollTop = chatbox.scrollHeight;
//     }
// }

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatbox = document.getElementById('chatbox');
    const message = userInput.value.trim();

    // Clear the input field after getting the message
    userInput.value = '';

    // Handle text message
    if (message) {
        await handleTextMessage(message, chatbox);
    }
}

async function handleTextMessage(message, chatbox) {
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

async function sendFile() {
    const fileInput = document.getElementById('fileInput');
    const chatbox = document.getElementById('chatbox');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Display a loading or processing message
        chatbox.innerHTML += `<div class="message user-message">Uploading file...</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        chatbox.innerHTML += `<div class="message bot-message">${data.response}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;

        // Clear the file input after processing
        fileInput.value = '';
    }
}

function showFileName() {
    var input = document.getElementById("file-input");
    var fileName = input.files[0].name;
    document.getElementById("file-name").textContent = fileName;
}

// Add an event listener to handle file selection
document.getElementById('fileInput').addEventListener('change', sendFile);
