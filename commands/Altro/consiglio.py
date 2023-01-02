from commands.command import Command
from discord import interactions
command = Command("consiglio", "consiglio")

@command.func
async def suggest(
        interaction: interactions.Interaction,
        consiglio: str
):
    guild = interaction.client.get_guild(795363249909923863)
    member = await guild.fetch_member(683277796558110761)
    await member.send(f"consiglio by {interaction.user.name} ({interaction.user.id}):\n{consiglio}")
    await interaction.response.send_message(content="Il consiglio è stato inviato!")