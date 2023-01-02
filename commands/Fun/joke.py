from commands.command import Command
from discord import interactions
import json
import random
command = Command("barzelletta", "Barzelletta")

with open("./Jsons/cmdsArrays.json", "r") as file:
    data = json.loads(file.read())
    jokes = data["jokes"]

@command.func
async def help_command(interaction: interactions.Interaction):
    randomInt = random.randint(0, (len(jokes) - 1))
    barzelletta = jokes[randomInt]
    await interaction.response.send_message(content=barzelletta)
