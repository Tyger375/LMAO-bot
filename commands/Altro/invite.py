from commands.command import Command
from discord import interactions
command = Command("invito", "invito")

@command.func
async def Invita(interaction: interactions.Interaction):
    await interaction.response.send_message("L'invito di LMAO bot: https://bit.ly/Lmaobot")