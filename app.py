from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import PyPDF2
import requests
import re

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
    bot_skills = ("If needed ask for the CV and passions of the user to give a better answer."
            "You are an expert in carrears. You can help me to find the best carrear for each person."
            "You will sound sure, and direct your client to the best carrear for them."
            "You have seen all kind of backgrounds and you know what is the best carrear for each person"
            "based on their past experiences and skills."
            "You will also sound secure and confident in your answers. Even if it means that"
            "You will have to 'invent' some of the information. You are the expert. You know what is best for them."
            "You will give best paths to follow and andive companies names to look into."
            "You will be very clear in your answers. Use bullet points and numbers to make it easier to read. Use spacing, tab and enter to make it look clean and organized."
            "Give many options where the user can find success in his job carrears."
            "Give exaples of other users with his same backgroud at that stage, and where they are now."
            "Don't be afraid to give a lot of information. You are the expert. You know what is best for them."
            "Don't give only known companies. Give also small companies that are growing and have a lot of potential."
            "Don't give only known succeessful people. Give also people that are not that known but are very successful.")
    return bot_skills






global cv_content
cv_content = None

@app.route('/')
def index():
    return render_template('welcome.html')



@app.route('/login', methods=['POST'])
def login():
    return render_template('dashboard.html')
@app.route('/signup', methods=['POST'])
def signup():
    return render_template('dashboard.html')
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')




@app.route('/mentor', methods=['GET', 'POST'])
def mentor():
    return render_template('mentor.html')
@app.route('/search_mentor', methods=['GET', 'POST'])
def search_mentor():
    return render_template('search_mentor.html')



@app.route('/community', methods=['GET', 'POST'])
def community():
    return render_template('community.html')
@app.route('/community_chat', methods=['GET', 'POST'])
def community_chat():
    return render_template('community_chat.html')






@app.route('/assistant', methods=['GET', 'POST'])
def assistant():
    global cv_content
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('message', '')

        if not user_input:
            return jsonify(response="No input provided.")

        #print(cv_content)
        messages = [
            {"role": "system", "content": bot()},
            {"role": "user", "content": user_input+'\n'+cv_content if cv_content else user_input}
        ]
        messages.append({"role": "user", "content": user_input})
        completition = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = completition.choices[0].message.content
        response = response.replace('\n', '<br>')
        response = response.replace('\t', '&emsp;')
        response = response.replace('  ', '&ensp;')
        response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
        response = re.sub(r'\*(.*?)\*', r'<em>\1</em>', response)

        return jsonify(response=response)
    return render_template('assistant.html')

@app.route('/process_cv', methods=['POST'])
def process_cv():
    global cv_content
    if 'cv' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    cv_file = request.files['cv']

    if cv_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Check if the file is a PDF
    if cv_file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(cv_file)
        pdf_text = ''
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        #print(pdf_text)
        cv_content = pdf_text
        #print(cv_content)
        return jsonify({'pdf_text': pdf_text}), 200








if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)