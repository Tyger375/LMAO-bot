from commands.command import Command
from discord import interactions, Embed, Color
from discord.ui import Button, View
import json
command = Command("bot-info", "bot-info")

with open("./Jsons/internal.json") as file:
    internal = json.loads(file.read())
version = internal["version"]

buttons = [
    ["Invito", "https://discord.com/oauth2/authorize?client_id=856159162466304040&permissions=2147875904&scope=bot%20applications.commands", "📧"],
    ["Server di supporto", "https://discord.gg/WVKC8kktEx", "🎮"],
    ["Votami su top.gg", "https://top.gg/bot/856159162466304040", "👍"]
]

@command.func
async def giochiamo(interaction: interactions.Interaction):
    embed = Embed(title="Info bot", color=Color.dark_red())\
    .add_field(name="Linguaggio", value="Python", inline=True)\
    .add_field(name="Developer", value="tyger 375#4141", inline=True)\
    .add_field(name="Libreria", value="discord.py", inline=True)\
    .add_field(name="Versione", value=version, inline=True)\
    .add_field(name="prefisso", value="slash commands", inline=True)\
    .add_field(name="Sito", value="https://lmaobot.gq/", inline=True)\
    .add_field(name="Ping", value=f'{round(interaction.client.latency * 1000)} ms', inline=True)

    view = View()
    for label, url, emoji in buttons:
        view.add_item(
            Button(
                label=label,
                url=url,
                emoji=emoji
            )
        )

    await interaction.response.send_message(content="", embed=embed, view=view)