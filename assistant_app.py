import openai
import hashlib
import base64
import os
from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Initialize OpenAI API key
openai.api_key = 'INSERT_OPENAI_API_KEY_HERE'

# Initialize Flask application
app = Flask(__name__)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Set up rate limiting
limiter = Limiter(app, key_func=lambda: g.user['id'])

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    api_key = db.Column(db.String(200), unique=True, nullable=False)
    subscription_level = db.Column(db.String(50), nullable=False, default='free')

    def __repr__(self):
        return f"User('{self.username}', '{self.subscription_level}')"

# Create tables
db.create_all()

# User authentication
def authenticate(request):
    api_key = request.headers.get('Authorization')
    if not api_key:
        return None

    user = User.query.filter_by(api_key=api_key).first()
    return user

# Update rate limits based on subscription level
@app.before_request
def set_rate_limit():
    user = authenticate(request)
    if user:
        g.user = {'id': user.id, 'subscription_level': user.subscription_level}
        if user.subscription_level == 'free':
            limiter.limit('10 per hour')(chatbot)
        elif user.subscription_level == 'pro':
            limiter.limit('500 per hour')(chatbot)
        elif user.subscription_level == 'enterprise':
            limiter.limit('5000 per hour')(chatbot)
    else:
        g.user = {'id': 'anonymous'}

# Define endpoint for chatbot API
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Authenticate user
    user = authenticate(request)
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401

    # Parse user input
    user_input = request.json.get('input', '')

    # Use natural language processing to generate chatbot response
    chatbot_response = generate_response(user_input)

    # Return chatbot response
    return jsonify({'response': chatbot_response})

# Generate chatbot response using OpenAI API
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

# Run Flask application
if __name__ == '__main__':
    app.run()
