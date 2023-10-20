import os
import requests
import openai
import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv("apikeys.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("Bot is now ready to use.")

class chatGPT:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def generate_respone(self, *arg):
        print(self.messages)
        self.messages.append({"role": "user", "content": " ".join(arg[0])})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        response_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response_message})

        return response_message
    def clear_context(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

chatBot = chatGPT()

@client.command(pass_context = True)
async def gpt(ctx, *arg):
    response = chatBot.generate_respone(arg)
    await ctx.send(response)

@client.command(pass_context = False)
async def gpt_clear(ctx):
    chatBot.clear_context()

client.run(BOT_TOKEN)