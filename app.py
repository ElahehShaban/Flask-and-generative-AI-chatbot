

from flask import Flask, request, jsonify, render_template
import openai
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
app = Flask(__name__)

# Replace with your actual OpenAI API key
openai.api_key =''  # Replace with your actual API key

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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

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
