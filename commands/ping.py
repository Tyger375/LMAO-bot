from commands.command import Command
from discord import interactions
command = Command("ping", "test ping")

@command.func
async def test(interaction: interactions.Interaction):
    await interaction.response.send_message("Ciao!")
