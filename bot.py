client_name = "Mānēs"
version = "0.3.1"

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
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('token')

# Client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"{client_name} ({version}) is online.")

## Commands
@tree.command(name="ping", description="Check response latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {client.latency * 1000:.2f} ms", ephemeral=True)

client.run(token)
