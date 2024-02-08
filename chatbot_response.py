import re
import long_responses as long
from create_memes import get_meme_templates, create_meme

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
    
    # calculate percent of recognized words in a user message 
    percentage = float(message_certainty)*( float(len(recognised_words)))
    
    for word in required_words:
        if word not in user_message:
            has_required_words = False 
            break

    if has_required_words or single_response: 
        return int(percentage*100) # simply converts percentage to an integer
    else: 
        return 0
    
def handle_meme_request(choice, text_top, text_bottom):
    templates = get_meme_templates()
    try: 
        selected_template = templates[int(choice)-1]
        return create_meme(selected_template['id'], text_top, text_bottom)
    except (ValueError, IndexError):
        return "Invalid choice or error creating meme."
        

"""
def handle_meme_request():
    templates = get_meme_templates()
    for i, template in enumerate(templates[:10], 1):
        print(f"{i}. {template['name']}")

    choice = input("Here are the current top 10 Memes. Please choose one (number): ")
    try:
        selected_template = templates[int(choice)-1]
    except (ValueError, IndexError):
        return "Choose something else, your choice is not valid."
    
    text_top = input("Top text: ")
    text_bottom = input("Bottom text: ")
    meme_url = create_meme(selected_template['id'], text_top, text_bottom)
    return meme_url
"""

def check_all_messages(message):
    highest_prob_list = {}
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    #### RESPONSES ####
    response('Hello! I\'m your (mostly friendly) meme bot (use a "-" between two statements for creating a meme).', ["hey", "hi", "Whats up", "hey there", "hello"], single_response=True)
    response("I\'m doing fine, and you? Do you want some memes", ['how', 'are', 'you'], required_words=['how'])
    response("I am a meme bot not a weather fairy", ["weather", "sunny", "rain", "forecast"])
    response("Sounds like you need a meme!", ["Can", "you", "help", "me"], required_words=["help"])
    response("You are welcome!", ["thanks", "thank you"])
    response("Please talk in full sentences with me.", ["ok", "okay", "sure", "yes", "no"], single_response=True)

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    #print(highest_prob_list)

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match 

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())

    if 'meme' in split_message or 'memes' in split_message:
        return handle_meme_request()
    
    response = check_all_messages(split_message)
    return response


# Testing response system
#while True:
#    print("Bot: " + get_response(input("You: ")))