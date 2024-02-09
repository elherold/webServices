
import random

def unknown():
    response = ['Could you please re-phrase that? ', 
                'I\'m not sure I understood you correctly',
                'Maybe look that up in a search engine of your choice',
                'Do I look like Chat GPT to you?', 
                'Are you sure you want a reply to that?']
    return random.choice(response)

def jokes():
    response = ['Why did the meme go to therapy? Because it couldn\'t handle the existential dread of its own virality.',
                'Why was the meme afraid of the dark? Because it couldn\'t go viral without being seen.',
                'Why don\'t memes make good secret agents? Because they\'re always being shared.',
                'Why don\'t memes pay taxes? Because they\'re always on the net.',
                'What\'s a meme\'s favorite place to visit? The \"front page of the internet.\"',
                'How do memes propose? \"Will you be the template to my caption?\"']
    return random.choice(response)