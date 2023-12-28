
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key here. Remember to keep it secure.
openai.api_key = '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'  # Replace with your actual API key

def get_openai_response(prompt, model="gpt-4-1106-preview", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    bot_response = get_openai_response(user_input)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
