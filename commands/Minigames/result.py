from firebase import firebase
from discord import Client
import json


with open("./Jsons/internal.json") as f:
    internal = json.loads(f.read())

firebase = firebase.FirebaseApplication(internal["firebase"], None)

async def getInfos(client: Client, Id):
    path = f"/ranks/{str(Id)}/"
    author = await client.fetch_user(Id)
    username = str(author).replace(f"#{author.discriminator}", "")
    return path, username

def createUser(authorId: str, username: str):
    firebase.put(f"/ranks/{authorId}/", "punteggio", 0)
    firebase.put(f"/ranks/{authorId}/", "livello", 0)
    firebase.put(f"/ranks/{authorId}/", "username", username)

async def Win(client: Client, Id):
    authorId = str(Id)
    path, username = await getInfos(client, Id)
    if firebase.get(path, "") is not None:
        newScore = int(firebase.get(path, "punteggio")) + 35
        if int(newScore) > 250:
            newLevel = int(firebase.get(path, "livello")) + 1
            firebase.put(path, "livello", newLevel)
            firebase.put(path, "punteggio", 0)
        else:
            firebase.put(path, "punteggio", newScore)
        firebase.put(path, "username", username)
    else:
        createUser(authorId, username)

async def Lose(client: Client, Id):
    authorId = str(Id)
    path, username = await getInfos(client, Id)
    if firebase.get(path, "") is not None:
        level = firebase.get(path, "livello")
        if level != 0:
            score = int(firebase.get(path, "punteggio"))
            score -= 25
            if score < 0:
                score += 250
                level -= 1
                firebase.put(path, "livello", level)
            firebase.put(path, "punteggio", score)
            firebase.put(path, "username", username)
    else:
        createUser(authorId, username)