# webServices
Project 3 AI in the web


## Implement some Chatbot fpr your channel:
We've implemented a "MemeBot". Users are prompted to provide two pieces of text, separated by a hyphen ("-"), which the bot then utilizes to generate memes. 
These text snippets serve as the top and bottom captions of a meme, matched with a randomly selected template accessed through the imgflip API. 
### Meme Generation
The MemeBot's core functionality revolves around meme creation. When a user submits a message containing a "-" delimiter, the bot interprets this as a cue to generate a meme. 
It splits the message at the hyphen to extract the intended top and bottom texts for the meme. A meme template is randomly chosen from a predefined list obtained via the imgflip API. The bot then creates a meme using these texts and the selected template
We see that this is not optimal and it would be better if the user could e.g. write two separate messages as the top and bottom texts. 
However, recognizing the complexity of managing stateful interactions in a distributed message environment and the scope for the project, we opted for this approach to meme generation as a compromise between functionality and technical feasibility.  
### Handling other user requests
Aside from meme generation, the MemeBot is equipped with basic logic to process and respond to user queries that do not involve meme creation. 
It employs keyword matching to identify the nature of the user's request, generating responses from a set of pre-written sentences.
