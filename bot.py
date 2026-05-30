client_name = "Bot_Name"
version = "0.1.5"

# Initialization
import os, sys, subprocess
def install():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
install()

import certifi
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('token')
guilds = [discord.Object(id=int(gid)) for gid in os.getenv('guilds', '').replace(' ', '').split(',') if gid]

# Client
intents = discord.Intents.default()
client = commands.Bot(command_prefix='?', intents=intents)

@client.event
async def on_ready():
    if guilds:
        for guild in guilds:
            synced = await client.tree.sync(guild=guild)
        command = ', '.join(command.name for command in synced) or 'none'
        print(f"Synced {len(synced)} guild command(s) to {len(guilds)} guild(s): {command}")
    print(f"{client_name} ({version}) is online.")

## Commands
@client.tree.command(name="ping", description="Check latency.")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {client.latency * 1000:.2f} ms", ephemeral=True)

client.run(token)
