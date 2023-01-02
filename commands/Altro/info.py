from commands.command import Command
from typing import Optional
from discord import interactions, User, Embed
import random
command = Command("info", "info")

types = ["Bot", "Persona"]
genders = ["Femmina", "Maschio"]
mesiTrenta = [11, 4, 6, 9]
aggettiviNegativi = ["cattivo", "egoista", "introverso", "antipatico", "pessimista", "arrogante"]
aggettiviPositivi = ["una persona", "uou", "divertente", "bravo", "onesto", "sincero"]

def createId():
    ID = ""
    for numero in range(18):
        ID += str(random.randint(1, 9))
    return ID

def valoriRandom():
    type = random.randint(0, 1)
    gender = random.randint(0, 1)
    adjectives = randomInfos()
    data, dataCreation = getDates()
    return type, gender, adjectives, data, dataCreation

def getDay(month):
    if month in mesiTrenta:
        day = random.randint(1, 30)
    elif month == 2:
        day = random.randint(1, 28)
    else:
        day = random.randint(1, 31)
    return day
def getDates():
    # Data born
    month = random.randint(1, 12)
    year = random.randint(1000, 2020)
    day = getDay(month)
    bornData = f"{day}/{month}/{year}"

    # Data created
    monthCreated = random.randint(1, 12)
    yearCreated = random.randint(1000, 2020)
    while year > yearCreated:
        yearCreated = random.randint(1000, 2020)
    dayCreated = getDay(monthCreated)

    dataCreated = f"{dayCreated}/{monthCreated}/{yearCreated}"
    return bornData, dataCreated

def randomInfos():
    adjectives = []
    negativeNumbers = []
    positiveNumbers = []
    for x in range(2):
        for y in range(3):
            if x == 1:
                numero = random.randint(0, (len(aggettiviNegativi) - 1))
                while numero in negativeNumbers:
                    numero = random.randint(0, (len(aggettiviNegativi) - 1))
                negativeNumbers.append(numero)
                adjectives.append(aggettiviNegativi[numero])
            else:
                numero = random.randint(0, (len(aggettiviPositivi) - 1))
                while numero in positiveNumbers:
                    numero = random.randint(0, (len(aggettiviPositivi) - 1))
                positiveNumbers.append(numero)
                adjectives.append(aggettiviPositivi[numero])

    aggettiviString = ""
    for elem in adjectives:
        if elem in adjectives[(len(adjectives) - 1)]:
            aggettiviString = aggettiviString + elem
        else:
            aggettiviString = aggettiviString + elem + "\n"

    return aggettiviString

@command.func
async def Info(
    interaction: interactions.Interaction,
    user: Optional[User]
):
    if user is None:
        user = interaction.user
    type, gender, adjectives, data, dataCreated = valoriRandom()
    embed = Embed(title=f"Info di {user.name}", color=0xFF5733)\
    .add_field(name="Persona/Bot", value=types[type])\
    .add_field(name="Genere", value=genders[gender])\
    .add_field(name="Id", value=createId())\
    .add_field(name="caratteristiche", value=adjectives)\
    .add_field(name="Nato il:", value=data)\
    .add_field(name="Account creato il:", value=dataCreated)
    await interaction.response.send_message(embed=embed)