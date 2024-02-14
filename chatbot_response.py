import re
import long_responses as long

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    """
    Calculate the probability of a message being relevant based on recognized words and required words.
    
    Args:
        user_message (list): List of words in the user's message.
        recognised_words (list): List of words recognized by the bot.
        single_response (bool, optional): Indicates if only a single response is expected. Defaults to False.
        required_words (list, optional): List of words required in the user's message for a valid response. Defaults to [].
    
    Returns:
        int: Probability of relevance as a percentage.
    """
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
    
    # calculate percent of recognized words in a user message 
    percentage = float(message_certainty)/( float(len(recognised_words)))
    
    for word in required_words:
        if word not in user_message:
            has_required_words = False 
            break

    if has_required_words or single_response: 
        return int(percentage*100) # simply converts percentage to an integer
    else: 
        return 0
        
def check_all_messages(message):
    """
    Check all messages and determine the best response.
    
    Args:
        message (list): List of words in the user's message.
    
    Returns:
        str: Best response to the user's message.
    """
    highest_prob_list = {}
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    #### RESPONSES ####
    response('Hello! I\'m your (mostly friendly) meme bot (use a "-" between two statements for creating a meme).', ["hey", "hi", "Whats up", "hey there", "hello"], single_response=True)
    response("I\'m doing fine, and you? Do you want some memes", ['how', 'are', 'you'], required_words=['how'])
    response("I am a meme bot not a weather fairy", ["weather", "sunny", "rain", "forecast"])
    response("Sounds like you need a meme! Just write \"-\" between the statements.", ["Can", "you", "help", "me"], required_words=["help"])
    response("You are welcome!", ["thanks", "thank you"])
    response("Please talk in full sentences with me.", ["ok", "okay", "sure", "yes", "no"], single_response=True)
    response("Please write a \"-\" between your statements and I can process it as a meme request", ["give", "me", "a", "meme"], required_words=['meme'])
    response(long.jokes(), ["tell", "me", "joke"], required_words=['joke'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match 

def get_response(user_input):
    """
    Get response based on user input.
    
    Args:
        user_input (str): User's input message.
    
    Returns:
        str: Bot's response to the user's input.
    """
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    
    response = check_all_messages(split_message)
    return response

