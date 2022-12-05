# Discord Joke Bot
- Group project 3 for CNIT 519 - Natural Language Technologies.
- Status : `Work in Progress`
## Dependencies
1. Install dependencies using `pip install -r requirements.text`
## Instructions to start the bot
1. Create a `.env` file with:
```
DISCORD_TOKEN=<DISCORD BOT TOKEN>
DISCORD_GUILD=<DISCORD GUILD ID>
```
2. Run `bot.py`.
3. Start sending messages to designated text channel.

## Usage (Discord)
1. Say `Tell me a joke about [something]` and it'll return a message from `bot_utils.say_joke()` 


## Problem Statement
```
For this group project, you are to use an existing conversational agent (Alexa or alike) to create a joke recommendation system. Your requirements are:

1. Ask a user what kind of jokes they like to hear (you can assume that they can say something like 'animals', 'professions,' etc.)
2. Use information that they specified to search for an existing joke that you used for Projects 1 or 2.
3. Use what you (or any other group, with their permission) created for projects 1 or 2.
4. Do use sound similarity, other than edit distance, between a category that a user provided and your sources and targets. 
5. If you cannot find a joke that fits the pattern exactly, use some kind of concept/word hierarchy (wordnet may work) to navigate to the most similar joke. 
6. Give user options to choose something else if you cannot find what they are happy with. 
7. Ask a user if they want a joke to be explained, and, if they do, provide the explanation. 
8. Your interaction should be at least 6-7 turns long. 

If you create a new account for the conversational agent, do not forget to disable it after your project is done. You will be required to submit your code for this submission. 
```

## To Do
1. Implement sound similarity with anything other than edit distance. 
2. Pass argument the (actual) joke generator.
3. Figure out what to do about `5` and `7`.  
 
