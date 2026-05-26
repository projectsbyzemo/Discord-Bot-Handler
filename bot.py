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
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('token')

# Client(s)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    print(f"{clientName} ({version}) is connected to Discord.")

client.run(token)
