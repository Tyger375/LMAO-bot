from commands.command import Command
from discord import interactions, Embed, Color
from firebase import firebase
import json
command = Command("ranks", "ranks")

with open("./Jsons/internal.json") as f:
    internal = json.loads(f.read())

firebase = firebase.FirebaseApplication(internal["firebase"], None)

def is_number(string: str) -> bool:
    try:
        int(string)
        return True
    except Exception:
        return False

async def SortPunteggiConId(scoresId: dict, Ranks) -> Embed:
    embed = Embed(title="Primi 5 utenti", color=Color.blue())
    sorted_by_val = {
        k: b
        for k, b in sorted(
            scoresId.items(),
            key=lambda element: element[1],
            reverse=True
        )
    }
    for utente in list(sorted_by_val.keys())[0:5]:
        embed.add_field(
            name=str(Ranks[utente]["username"]),
            value=
            f"""
            livello: `{Ranks[utente]['livello']}`
            punteggio: `{Ranks[utente]["punteggio"]}`
            """,
            inline=False
        )
    return embed

@command.func
async def ranks(interaction: interactions.Interaction):
    await interaction.response.send_message("Ok! questa operazione potrebbe richiedere un po' di tempo...")
    Ranks = firebase.get("/ranks/", "")
    scoresId = {}
    for player in Ranks:
        if is_number(player):
            level = str(Ranks[player]["livello"])
            punteggio = str(Ranks[player]["punteggio"])
            length = len(punteggio)
            if length == 1:
                Tot = f"{level}00{punteggio}"
            elif length == 2:
                Tot = f"{level}0{punteggio}"
            else:
                Tot = f"{level}{punteggio}"
            scoresId[player] = int(Tot)

    message = await interaction.original_response()
    await message.edit(content="", embed=await SortPunteggiConId(scoresId, Ranks))