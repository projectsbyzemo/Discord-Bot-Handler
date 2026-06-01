# Initialization
import asyncio, os, sys, subprocess
def install():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
install()

if os.name == "nt":
    import msvcrt
else:
    import termios, tty
async def wait_for_escape():
    if os.name == "nt":
        while True:
            if msvcrt.kbhit() and msvcrt.getch() == b"\x1b":
                return
            await asyncio.sleep(0.05)

    loop = asyncio.get_running_loop()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    escape_pressed = loop.create_future()

    def on_stdin_ready():
        if sys.stdin.read(1) == "\x1b" and not escape_pressed.done():
            escape_pressed.set_result(None)

    try:
        tty.setcbreak(fd)
        loop.add_reader(fd, on_stdin_ready)
        await escape_pressed
    finally:
        loop.remove_reader(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
async def stop_on_escape():
    if not sys.stdin.isatty():
        print("ESC stop is unavailable because stdin is not interactive. Use Ctrl+C to stop.")
        return

    print("Press ESC to stop the bot.")
    await wait_for_escape()
    print("ESC pressed. Stopping bot...")
    await client.close()

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
    print(f"{os.getenv('client')} ({os.getenv('version')}) is online.")
    if not hasattr(client, "escape_stop_task"):
        client.escape_stop_task = asyncio.create_task(stop_on_escape())

## Ephemeral Commands
@tree.command(name="ping", description="Check the bot's response latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {client.latency * 1000:.2f} ms", ephemeral=True)

@tree.command(name="version", description="Check the bot's version.")
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(f"Version: {os.getenv('version')}", ephemeral=True)

@tree.command(name="purge", description="Delete a specified number of messages.")
@app_commands.describe(amount="Delete 1 to 100 messages.") 
@app_commands.guild_only()
async def purge(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
    await interaction.response.defer(ephemeral=True, thinking=True)
    try:
        deleted = await interaction.channel.purge(limit=amount)
    except discord.Forbidden:
        await interaction.followup.send("I need Manage Messages in this channel.", ephemeral=True)
        return
    except discord.HTTPException as error:
        await interaction.followup.send(f"Discord rejected the purge request: {error}", ephemeral=True)
        return

    await interaction.followup.send(f"Purged {len(deleted)} messages.", ephemeral=True)

client.run(token)
