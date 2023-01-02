from commands.command import Command
from discord import interactions, Embed, Color
from firebase import firebase
import datetime
import requests
import json
import Cmds.Error as Error
command = Command("daily", "Get your daily lmao-points")

with open("./Jsons/internal.json") as f:
    internal = json.loads(f.read())

firebase = firebase.FirebaseApplication(internal["firebase"], None)
topgg = internal["topgg"]

@command.func
async def daily(interaction: interactions.Interaction):
    userId = str(interaction.user.id)
    database = firebase.get("/economy/", userId)
    hours = 0
    if database is not None:
        lastDaily = database["daily"]
        lastDaily = datetime.datetime(
            lastDaily["year"],
            lastDaily["month"],
            lastDaily["day"],
            lastDaily["hour"],
            lastDaily["minute"],
            lastDaily["second"]
        )
        now = datetime.datetime.now()
        now = datetime.datetime(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        )
        remaining = now - lastDaily
        hours = remaining.total_seconds() / 3600
    if database is None or hours > 24:
        user = firebase.get("/ranks/", userId)
        author = interaction.user
        if user is None:
            return await interaction.response.send_message(
                embed=Error.Errore(
                    author=author,
                    errore="<:lmao:879736392144531536> Prima di riscattare i tuoi punti giornalieri, gioca ad un minigioco lmao bot"
                )
            )
        await interaction.response.defer()
        path = f"/ranks/{userId}"
        username = author.name.replace(f"#{author.discriminator}", "")
        data = {
            "Authorization": f"{topgg}"
        }
        request = requests.get("https://top.gg/api/bots/856159162466304040/check", headers=data, params={
            "userId": userId
        })
        if request.json()["voted"] == 0:
            pointsToAdd = 5
        else:
            pointsToAdd = 15
        if user is not None:
            level = int(user["livello"])
            score = int(user["punteggio"])
            score += pointsToAdd
            if score > 250:
                level += 1
                score = 0
                firebase.put(path, "livello", level)
            firebase.put(path, "punteggio", score)
            firebase.put(path, "username", username)
        time = datetime.datetime.now()
        data = {
            "year": time.year,
            "month": time.month,
            "day": time.day,
            "hour": time.hour,
            "minute": time.minute,
            "second": time.second
        }
        firebase.put(f"/economy/{userId}/", "daily", data)
        embed = Embed(color=Color.gold())\
        .set_author(icon_url=author.avatar.url, name=f"[Fatto!] {author.name}")
        content = """
            Hai riscattato i tuoi punti giornalieri!!
            """
        if pointsToAdd == 5:
            content += "\n Ricordati che puoi ricevere più punti giornalieri votando il bot su [top.gg](https://top.gg/bot/856159162466304040/vote)!"
        embed.description = content
        message = await interaction.original_response()
        await message.edit(embed=embed)
    else:
        await interaction.response.send_message(
            embed=
                Error.Errore(
                    author=interaction.user,
                    errore="<:lmao:879736392144531536> Hai già riscattato i tuoi punti giornalieri, aspetta `%.2f` ore" % (24 - hours)
                )
        )