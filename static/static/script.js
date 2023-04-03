const chatlog = document.getElementById('chatlog');
const user_input = document.getElementById('user_input');
const submit_button = document.getElementById('submit_button');

// Send user input to server and display chatbot response
function send_message() {
    const input_text = user_input.value.trim();

    if (input_text.length === 0) {
        return;
    }

    const request_data = {
        input: input_text
    };

    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request_data)
    })
    .then(response => response.json())
    .then(data => {
        const chatbot_response = data.response;
        display_message(input_text, 'user');
        display_message(chatbot_response, 'chatbot');
    })
    .catch(error => console.error(error));

    user_input.value = '';
}

// Display message in chat log
function display_message(message_text, message_sender) {
    const message = document.createElement('div');
    message.classList.add('message');
    message.classList.add(message_sender);
    message.innerText = message_text;
    chatlog.appendChild(message);
    chatlog.scrollTop = chatlog.scrollHeight;
}

// Send message when user clicks Send button or presses Enter
submit_button.addEventListener('click', send_message);
user_input.addEventListener('keydown', event => {
    if (event.code === 'Enter') {
        send_message();
    }
});
