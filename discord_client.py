""" 
    This is an implementation of a Discord Client based on the class handout FAQ bot with custom modifications by 
    Serhii Ivanchuk [000818168], Mohawk College, (updated) October 23, 2023
    
    C:\ProgramData\anaconda3\python.exe -m pip install discord
    
"""

import discord
from faq_bot import *

## DiscordClient Class Definition


class DiscordClient(discord.Client):
    """Class to represent the Client (bot user)"""

    # keep track if user returned back
    keepConversation = True

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print("Logged on as", self.user)
        if not load_FAQ_data():
            print("Exiting program...\n")
            exit()

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        # process user input and get a response message
        keep_conversation, response = process_input(message.content)

        # check if user came back, then send additional message
        if (self.keepConversation == False) and (keep_conversation == True):
            response = "Welcome back!\n" + response

        self.keepConversation = keep_conversation

        # send the response
        await message.channel.send(response)


## Set up and log in
client = DiscordClient()
with open("bot_token.txt") as file:
    token = file.read()
client.run(token)
