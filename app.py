

from flask import Flask, request, jsonify, render_template
import openai
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
load_dotenv()  # This line will load the .env file


app = Flask(__name__)

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
print("API Key:", os.getenv('OPENAI_API_KEY'))

def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  # The chat model identifier
        temperature=0.7, 
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()


@app.route('/')
def index():
    return render_template('index.html')

def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return str(e)

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = ' '.join(soup.stripped_strings)
    return text

def find_url_in_text(text):
    # This regex pattern might need adjustments based on the URLs you expect
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None


# Regular expressions for detecting sensitive information
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
NAME_REGEX = re.compile(r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b')  # Simple regex for names

def contains_sensitive_info(text):
    # Check for email addresses
    if EMAIL_REGEX.search(text):
        return True
    # Check for names (This is a basic check; might need more complex handling)
    if NAME_REGEX.search(text):
        return True
    # Add more checks as needed
    return False


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

    # Check for sensitive information
    if contains_sensitive_info(user_input):
        return jsonify({'response': 'Your query includes sensitive information.'})


    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    extracted_url = find_url_in_text(user_input)
    if extracted_url:
        html_content = fetch_url_content(extracted_url)
        extracted_text = extract_text_from_html(html_content)
        prompt = f"{user_input.replace(extracted_url, '')} Here is the content: {extracted_text}"
    else:
        prompt = user_input

    bot_response = get_openai_response(prompt)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
