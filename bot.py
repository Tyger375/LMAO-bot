import json
import os
import discord
from discord import app_commands
from firebase import firebase
import commands.command

with open("./Jsons/internal.json") as file:
    internal = json.loads(file.read())
firebase = firebase.FirebaseApplication(internal["firebase"], None)

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

# Register slash commands in these guilds
guilds = [
    discord.Object(id=795363249909923863),
    discord.Object(id=857988991692046346)
]

# importing "command" variable from modules
def _import(name):
    mod = __import__(name, fromlist=['command'])
    Class = getattr(mod, "command")
    return Class

# Registering slash command
def addCommand(name: str):
    module = f"commands.{name[:-3]}"
    print(f"importing module: {module}")
    try:
        commandClass: commands.command.Command = _import(module)
    except Exception as e:
        return print("error while importing:", module, e)

    tree.add_command(
        app_commands.Command(
            name=commandClass.name,
            description=commandClass.description,
            callback=commandClass.fn
        ),
        guilds=guilds
    )

# Add slash commands
def addCommands():
    # Looking for files into "commands" folder
    for item in os.scandir("commands"):
        if item.name == "command.py":
            continue
        if item.is_dir():
            if item.name == "__pycache__":
                continue
            for item2 in os.scandir(f"commands/{item.name}"):
                if item2.is_dir():
                    continue
                module = f"{item.name}.{item2.name}"
                addCommand(module)
        else:
            addCommand(item.name)

@client.event
async def on_ready():
    for guild in guilds:
        await tree.sync(guild=guild)
    print(f'We have logged in as {client.user}')

if __name__ == "__main__":
    addCommands()
    client.run("TOKEN")
