from commands.command import Command
from discord import interactions, Embed, Color
import random
command = Command("aiutami", "aiutami")

Yes = [
    "Secondo me si",
    "assolutamente si",
    "credo proprio di si",
    "la risposta è sicuramente si",
]
No = [
    "Non credo proprio",
    "Assolutamente no",
    "credo proprio di no",
    "sicuramente no",
]
Maybe = [
    "Forse",
    "Forse si... o forse no...",
    "Chiedimelo domani...",
    "Non sono sicuro della risposta",
]

def Ball8() -> str:
    SiNo = random.randint(1,3)

    if SiNo == 1:
        response = Yes[random.randint(1, len(Yes) - 1)]
    elif SiNo == 2:
        response = No[random.randint(1, len(No) - 1)]
    else:
        response = Maybe[random.randint(1, len(Maybe) - 1)]
    return response

@command.func
async def helpme(
        interaction: interactions.Interaction,
        messaggio: str
):
    response = Ball8()
    embed = Embed(title=f"Aiuto per **{interaction.user.name}**", color=Color.gold())\
    .add_field(name="Domanda", value=messaggio, inline=False)\
    .add_field(name="Risposta", value=response)
    await interaction.response.send_message(embed=embed)