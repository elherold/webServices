## channel.py - a simple message channel
##

from flask import Flask, request, render_template, jsonify, session
import json
import requests
import random
from chatbot_response import*
from flask_session import Session
from flask_cors import CORS
from redis import Redis

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False 
    SESSION_USE_SIGNER = True
    

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db




HUB_URL = 'http://localhost:5555'
HUB_AUTHKEY = '1234567890'
CHANNEL_AUTHKEY = '0987654321'
CHANNEL_NAME = "The One and Only Channel"
CHANNEL_ENDPOINT = "http://localhost:5001" # don't forget to adjust in the bottom of the file
CHANNEL_FILE = 'messages.json'

@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT

    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                             data=json.dumps({
            "name": CHANNEL_NAME,
            "endpoint": CHANNEL_ENDPOINT,
            "authkey": CHANNEL_AUTHKEY}))

    if response.status_code != 200:
        print("Error creating channel: "+str(response.status_code))
        return

def check_authorization(request):
    global CHANNEL_AUTHKEY
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        return False
    return True

@app.route('/health', methods=['GET'])
def health_check():
    global CHANNEL_NAME
    if not check_authorization(request):
        return "Invalid authorization", 400
    return jsonify({'name':CHANNEL_NAME}),  200

# GET: Return list of messages
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization", 400
    # fetch channels from server
    return jsonify(read_messages())

# POST: Send a message
@app.route('/', methods=['POST'])
def send_message():
    if 'state' not in session:
        print("no state in session 1")
    # fetch channels from server
    # check authorization header
    if not check_authorization(request):
        return "Invalid authorization", 400
    # check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if not 'content' in message:
        return "No content", 400
    if not 'sender' in message:
        return "No sender", 400
    if not 'timestamp' in message:
        return "No timestamp", 400

    content = message['content']

    if '-' in content:
        contents = content.split('-')
        bottom_text = contents[0]
        top_text = contents[1]
        templates = get_meme_templates()
        selected_template = random.choice(templates)
        response = create_meme(selected_template['id'], bottom_text , top_text)
    else:
        response = generate_response(content)

        # Save the original message
    messages = read_messages()
    messages.append({'content': message['content'], 'sender': message['sender'], 'timestamp': message['timestamp']})
    
    # save the generated response as a new message from the channel itself
    messages.append({'content': response, 'sender': CHANNEL_NAME, 'timestamp': message['timestamp']})
    
    save_messages(messages)
    return "OK", 200

"""
    # Check if we're starting a new meme creation process
    if 'state' not in session:
        # Save the top text and update the state
        session['top_text'] = content
        session['state'] = 'AWAITING_BOTTOM_TEXT'
        print("No state in session2")
        print("Entered AWAITING_TOP_TEXT state!")
        response = "Please enter the bottom text for your meme next!"

    elif session['state'] == 'AWAITING_BOTTOM_TEXT':
        # We have the top text saved now save the bottom text
        bottom_text = content
        templates = get_meme_templates()
        selected_template = random.choice(templates)
        print("Entered AWAITING_BOTTOM_TEXT state!")
        # Generate the meme using the saved top text, bottom text, and selected template
        response = create_meme(selected_template, session['top_text'], bottom_text)
        
        # Clear the session for next time
        session.pop('state', None)
        session.pop('top_text', None)
"""

def read_messages():
    global CHANNEL_FILE
    try:
        f = open(CHANNEL_FILE, 'r')
    except FileNotFoundError:
        return []
    try:
        messages = json.load(f)
    except json.decoder.JSONDecodeError:
        messages = []
    f.close()
    return messages 

def save_messages(messages):
    global CHANNEL_FILE
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)

def generate_response(input_message):
    try: 
        response = get_response(input_message)
        return response
    except Exception as e:
        return "Sorry, I cannot process your input right now. "

# Start development web server
if __name__ == '__main__':
    app.run(port=5001, debug=True)
