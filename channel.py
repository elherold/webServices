## channel.py - a simple message channel
##

from flask import Flask, request, render_template, jsonify
import json
import requests
import random
from chatbot_response import*
from create_memes import get_meme_templates, create_meme

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

HUB_URL = 'https://temporary-server.de'
HUB_AUTHKEY = 'Crr-K3d-2N'
CHANNEL_AUTHKEY = '0987654321'
CHANNEL_NAME = "MemeForge3000"
CHANNEL_ENDPOINT = "http://vm150.rz.uni-osnabrueck.de/user168/channel.wsgi" # don't forget to adjust in the bottom of the file
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

# Check if content includes a '-' to determine if it's intended for meme generation.
    if '-' in content:
        # Split content at '-' to get separate texts for the bottom and top of the meme.
        contents = content.split('-')
        bottom_text = contents[0]
        top_text = contents[1]
        # Get a list of meme templates and select one randomly.
        templates = get_meme_templates()
        selected_template = random.choice(templates)
        # Create a meme with the selected template and specified texts.
        response = create_meme(selected_template['id'], bottom_text, top_text)
    else:
        # If '-' is not in content, generate a response without meme creation.
        response = generate_response(content)

        # Save the original message
    messages = read_messages()
    messages.append({'content': message['content'], 'sender': message['sender'], 'timestamp': message['timestamp']})
    
    # save the generated response as a new message from the channel itself
    messages.append({'content': response, 'sender': CHANNEL_NAME, 'timestamp': message['timestamp']})
    
    save_messages(messages)
    return "OK", 200

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
