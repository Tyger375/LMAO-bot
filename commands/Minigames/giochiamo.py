from commands.command import Command
from typing import Literal
from discord import interactions
from commands.Minigames.headsTails import headsTails
from commands.Minigames.RockPaperScissor import SCF
from commands.Minigames.future import future
from commands.Minigames.akiCmd import Aki
command = Command("giochiamo", "giochiamo")

@command.func
async def giochiamo(
        interaction: interactions.Interaction,
        game: Literal["scf", "testa", "croce", "futuro", "akinator"]
):
    # interaction.guild.id
    if game in ["testa", "croce"]:
        await headsTails(interaction, game)
    elif game == "futuro":
        await future(interactions.InteractionResponse(interaction))
    elif game == "scf":
        await SCF(interaction)
    elif game == "akinator":
        await Aki(interaction)
    else:
        await interaction.response.send_message("In progress")
