from discord import Embed, Color
from discord.interactions import Interaction
from commands.Minigames.result import Win, Lose
import random
import asyncio

cases = [
    "testa",
    "croce"
]

async def headsTails(interaction: Interaction, move: str):
    embed = Embed(title="LMAO Bot", color=Color.gold())\
    .add_field(name="La mossa del player", value=move, inline=False)\
    .add_field(name="La mossa del bot", value="In attesa...", inline=False)\
    .add_field(name="Risultato", value="In attesa...", inline=False)

    await interaction.response.send_message(embed=embed)

    await asyncio.sleep(2)

    case = cases[random.randint(0,1)]
    embed.clear_fields()
    embed\
    .add_field(name="La mossa del player", value=move, inline=False) \
    .add_field(name="La mossa del bot", value=case, inline=False)
    if move == case:
        embed.add_field(name="Risultato", value="Hai vinto!", inline=False)
        asyncio.create_task(Win(interaction.client, interaction.user.id))
    else:
        embed.add_field(name="Risultato", value="Hai perso!", inline=False)
        asyncio.create_task(Lose(interaction.client, interaction.user.id))

    message = await interaction.original_response()
    await message.edit(embed=embed)