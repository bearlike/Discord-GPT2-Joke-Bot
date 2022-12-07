#!/usr/bin/env python3
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
        send_message = "Hello, Do you want me to tell a joke?\nJust say `Tell me a joke about [something]`."

        if str(message.content).startswith("Tell me a joke about"):
            keyword = (message.content).replace("Tell me a joke about ", "")
            post_obj = {
                "topic": keyword
            }
            x = requests.post(
                "http://localhost:5000/api/generate/joke/", data=post_obj)
            send_message = x.json()["message"]

        await message.channel.send(send_message)

if __name__ == "__main__":
    client.run(TOKEN)
