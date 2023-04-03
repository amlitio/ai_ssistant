from flask import g
from models import User
import openai

def authenticate(request):
    api_key = request.headers.get('Authorization')
    if not api_key:
        return None

    user = User.query.filter_by(api_key=api_key).first()
    return user

def set_rate_limit():
    user = authenticate(request)
    if user:
        g.user = {'id': user.id, 'subscription_level': user.subscription_level}
    else:
        g.user = {'id': 'anonymous'}

def generate_response(user_input):
    # Prepare message for the chat model
    messages = [{'role': 'system', 'content': 'You are a helpful AI chatbot.'},
                {'role': 'user', 'content': user_input}]

    # Query OpenAI API for response
    response = openai.ChatCompletion.create(
        model='gpt-4.5-turbo',
        messages=messages,
        max_tokens=60,
        n=1,
        temperature=0.5,
    )

    # Extract chatbot response
    chatbot_response = response.choices[0].text.strip()

    # Return chatbot response
    return chatbot_response
