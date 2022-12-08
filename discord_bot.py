#!/usr/bin/env python3
""" Discord bot that wraps around the RESTful API server (server.py)
"""
import os
import requests
import re
import discord
from dotenv import load_dotenv
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents(
    messages=True,
    guilds=True,
    message_content=True
)
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'\n{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


@client.event
async def on_message(message):
    if message.channel.name == "talk-to-bot":
        print(f"Message: {message.content}")
        if message.author == client.user:
            return
        regex = r"Tell me a joke about [a-zA-Z0-9]+"
        # author = message.author.name
        send_message = \
            """
        ```
┌────────────────────────────────────────────────────────────────┐
│ Fancy some humor?                                              │
│ ─────────────────                                              │
│ Usage:                                                         │
├─────────────────────────────────────┬──────────────────────────┤
│ 1. Tell me a joke about [something] │ Generates a joke using   │
│                                     │ fine-tuned GPT-2         │
├─────────────────────────────────────┼──────────────────────────┤
│ 2. Find me a pun about [something]  │ Retrieve and explains a  │
│                                     │ pun.                     │
└─────────────────────────────────────┴──────────────────────────┘
```
        """
        input_phrase = str(message.content).lower()
        if input_phrase.startswith("tell me a joke about"):
            keyword = input_phrase.replace("tell me a joke about ", "")
            post_obj = {
                "topic": keyword
            }
            x = requests.post(
                "https://519.thekrishna.in/api/joker/generator/", data=post_obj)
            send_message = x.json()["joke"]

        elif input_phrase.startswith("find me a pun about"):
            keyword = input_phrase.replace("find me a pun about ", "")
            post_obj = {
                "topic": keyword
            }
            x = requests.post(
                "https://519.thekrishna.in/api/joker/finder/", data=post_obj)
            response = x.json()
            joke, explaination = response["joke"], response["explaination"]
            send_message = f"- **Pun**: `{ joke }`\n- **Explaination**: { explaination }"

        await message.channel.send(send_message)

if __name__ == "__main__":
    client.run(TOKEN)
