#!/usr/bin/env python3
import os
import re
import discord
from bot_utils import Utils
from dotenv import load_dotenv
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
utils = Utils()
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
            send_message = utils.say_joke(keyword)

        await message.channel.send(send_message)

if __name__ == "__main__":
    client.run(TOKEN)
