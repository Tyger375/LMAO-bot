from commands.command import Command
from discord import interactions
import json
import random
import asyncio
command = Command("indovinello", "indovinello")

with open("./Jsons/cmdsArrays.json", "r") as file:
    data = json.loads(file.read())
    riddles = data["riddles"]

@command.func
async def help_command(interaction: interactions.Interaction):
    randomInt = random.randint(0, (len(riddles) - 1))
    riddle = riddles[randomInt]

    question: str = riddle["indovinello"]
    answer = riddle["risposta"]

    await interaction.response.send_message(content=question.encode("utf-8").decode('utf-8'))
    message = await interaction.original_response()
    await asyncio.sleep(2)
    await message.edit(content=f"{message.content}\n{answer}")
