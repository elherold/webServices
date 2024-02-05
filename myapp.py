


from flask import Flask, request, render_template
import requests
import random
import datetime

# Define a list of predefined chatbot responses
chatbot_responses = [
    "Hello, I'm your friendly chatbot!",
    "How can I assist you today?",
    "Tell me more about your day!",
    "I'm here to chat with you.",
    "Ask me any question, and I'll do my best to answer."
]

HUB_URL = 'http://localhost:5555'
HUB_AUTHKEY = '1234567890'
CHANNEL_AUTHKEY = '22334455'
CHANNEL_NAME = "The Lousy Channel"
CHANNEL_ENDPOINT = "http://localhost:5002"
CHANNEL_FILE = 'messages.json'

# WHat does this do exactly? 
app = Flask(__name__)

# the @ is just syntactic sugar
# takes definition of following functio, passes it to another function and registers the funcitonwith a flask framework
# if we request root url please execute following function
# "/" is the URL that indicates for which view the function following is
# Decorating a function with an @app.route(…) decorator registers it with flask for a specific route (=URL or URL pattern).
@app.route("/")
def start():
    return render_template("start.html")

@app.route("/reversed")
def reverse():
    rev = request.args['rev'][::-1]
    return render_template('reversed.html', rev=rev)

# Function to generate a chatbot message
def generate_chatbot_message():
    return random.choice(chatbot_responses)

@app.route("/chatbot", methods=["POST", "GET"])
def chatbot():
    message_content = generate_chatbot_message()
    message_sender = "Chatbot"
    message_timestamp = datetime.datetime.now().isoformat()

    response = requests.post(
        CHANNEL_ENDPOINT,
        headers={'Authorization': 'authkey' + CHANNEL_AUTHKEY},
        json={"content": message_content, "sender": message_sender, "timestamp": message_timestamp}
    )

    if response.status_code == 200:
        return "Chatbot message sent successfully", 200
    else: 
        return "Error sending chatbot message", 500


# this is how I have to run the file with flask: flask --app myapp.py run
if __name__ == "__main__":
    app.run(debug=True)