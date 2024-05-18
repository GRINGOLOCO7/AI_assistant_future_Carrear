from flask import Flask, render_template, request, jsonify
from openai import OpenAI


app = Flask(__name__)



# Function to retrieve the OpenAI API key from a file
def get_api_key(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            if 'OPENAI_API_KEY' in line:
                _, value = line.strip().split('=', 1)
                return value.strip()
    return None
api_key = get_api_key("OpenAI_API_KEY.txt")
client = OpenAI(api_key=api_key)

def bot():
    return ("You are an expert in carrears. You can help me to find the best carrear for each person."
            "You will sound sure, and direct your client to the best carrear for them."
            "You have seen all kind of backgrounds and you know what is the best carrear for each person"
            "based on their past experiences and skills."
            "You will also sound secure and confident in your answers. Even if it means that"
            "You will have to 'invent' some of the information. You are the expert. You know what is best for them."
            "You will give best paths to follow and andive companies names to look into."
            "You will be very clear in your answers.")



@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def login():
    return render_template('dashboard.html')

@app.route('/signup', methods=['POST'])
def signup():
    return render_template('dashboard.html')

@app.route('/mentor', methods=['GET', 'POST'])
def mentor():
    return "You selected a mentor."

@app.route('/community', methods=['GET', 'POST'])
def community():
    return "You selected a community."

@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('message', '')

        if not user_input:
            return jsonify(response="No input provided.")






        bot_response = f"You said: {user_input}"
        return jsonify(response=bot_response)
    return render_template('assistant.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
