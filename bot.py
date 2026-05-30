clientName = "Bot_Name"
version = "0.0.1"

# Initialization
import os, sys, subprocess
def install():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
install()

import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('token')

# Client
intents = discord.Intents.default()
client = commands.Bot(command_prefix='?', intents=intents)

@client.event 
async def on_ready():
    print(f"{clientName} ({version}) is online.")

## Commands
@client.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {client.latency * 1000:.2f} ms ||{ctx.author.mention}||")

client.run(token)
