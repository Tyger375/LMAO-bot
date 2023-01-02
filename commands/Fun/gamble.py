from commands.command import Command
from typing import Literal
from discord import interactions, Embed, Color
from commands.Minigames.result import Win, Lose
import random
command = Command("scommetto", "scommetto")

@command.func
async def gamble(
    interaction: interactions.Interaction,
    numero: Literal["1", "2", "3", "4", "5", "6"]
):
    number = int(numero)
    randomNum = random.randint(1, 6)
    embed = Embed(title="LMAO Bot", color=Color.gold())\
    .add_field(name="La tua scelta", value=numero, inline=False)\
    .add_field(name="La scelta del bot", value="In attesa...", inline=False)\
    .add_field(name="Risultato", value="In attesa...", inline=False)

    await interaction.response.send_message(embed=embed)

    embed.clear_fields()
    embed.add_field(name="La tua scelta", value=numero, inline=False)\
    .add_field(name="La scelta del bot", value=str(randomNum), inline=False)

    client = interaction.client
    userId = interaction.user.id
    if randomNum == number:
        embed.add_field(name="Risultato", value="Hai vinto!", inline=False)
        await Win(client, userId)
    else:
        embed.add_field(name="Risultato", value="Hai perso!", inline=False)
        await Lose(client, userId)

    message = await interaction.original_response()

    await message.edit(embed=embed)