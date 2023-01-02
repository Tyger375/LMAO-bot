from commands.command import Command
from typing import Optional
from discord import interactions, File
from firebase import firebase
import json
import Cmds.Error as Error
from PIL import ImageFont
from commands.Images.generate import *
command = Command("rank", "rank")

with open("./Jsons/internal.json") as f:
    internal = json.loads(f.read())

firebase = firebase.FirebaseApplication(internal["firebase"], None)

palettes = {
    "./wallpapers/7809.jpg":{
        "Colore1":(0,0,0),
        "Colore2":(255,255,255),
        "Colore3":(255,255,255)
    },
    "./wallpapers/92758.jpg":{
        "Colore1":(0,0,0),
        "Colore2":(255,255,255),
        "Colore3":(255,255,255)
    },
    "./wallpapers/82816.jpg":{
        "Colore1":(255,255,255),
        "Colore2":(255,255,255),
        "Colore3":(255,255,255)
    },
    "./wallpapers/89236.jpg":{
        "Colore1":(0,0,0),
        "Colore2":(0,0,0),
        "Colore3":(0,0,0)
    },
    "./wallpapers/92366.jpg":{
        "Colore1":(255,255,255),
        "Colore2":(255,0,0),
        "Colore3":(255,0,0)
    },
    "./wallpapers/75125.jpg":{
        "Colore1":(255,255,255),
        "Colore2":(255,0,0),
        "Colore3":(255,0,0)
    },
    "./wallpapers/93725.jpg":{
        "Colore1":(255,255,255),
        "Colore2":(255,0,0),
        "Colore3":(255,0,0)
    }
}

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 300
AVATAR_SIZE = 128

@command.func
async def rank(
    interaction: interactions.Interaction,
    user: Optional[User]=None
):
    if user is None:
        user = interaction.user
    await interaction.response.defer()
    message = await interaction.original_response()
    username = user.name
    score = firebase.get(f"/ranks/{str(user.id)}/", "punteggio")
    if score is None:
        return await message.edit(
            embed=Error.Errore(
                interaction.user, "L'utente non ha un punteggio"
            )
        )
    score = int(score)
    level = int(firebase.get(f"/ranks/{str(user.id)}/", "livello"))

    wallpaper = firebase.get(f"/ranks/{str(user.id)}/", "SfondoAttuale")

    img: Image
    draw: ImageDraw

    if wallpaper is None or wallpaper == "default":
        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, IMAGE_WIDTH, IMAGE_HEIGHT), fill=(0, 0, 0), outline=(0, 0, 0))
        draw.rectangle((25, 25, IMAGE_WIDTH - 25, IMAGE_HEIGHT - 25), fill=(146, 153, 255))
        color1 = (0, 0, 0)
        color2 = (0, 0, 0)
        color3 = (0, 0, 0)
    else:
        img = getBasic(wallpaper, (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)
        color1 = palettes[wallpaper]["Colore1"]
        color2 = palettes[wallpaper]["Colore2"]
        color3 = palettes[wallpaper]["Colore3"]

    avatar_image = await getAvatar(user, AVATAR_SIZE)

    posX = (IMAGE_WIDTH - AVATAR_SIZE) // 10
    posY = (IMAGE_HEIGHT - AVATAR_SIZE) // 2

    img.paste(
        avatar_image,
        (posX, posY),
        roundAvatar(AVATAR_SIZE)
    )

    # Score bar
    draw.rectangle(
        (175, 200, ((score + 50) + 175), 220),
        fill=(0, 250, 0),
        outline=(150, 150, 0)
    )

    # Adding texts
    # First text
    text = "Rank di:"
    fontTitle = ImageFont.truetype('arial.ttf', 55)
    text_width, text_height = draw.textsize(text, font=fontTitle)

    # Setting position
    titleX = (IMAGE_WIDTH - text_width) // 2
    titleY = ((IMAGE_HEIGHT - text_height) // 5) - 15
    draw.text(
        (titleX, titleY),
        text,
        fill=color1,
        font=fontTitle
    )

    # Second text
    textUser = str(username)
    fontUser = ImageFont.truetype('arial.ttf', 35)
    text_widthUser, text_heightUser = draw.textsize(textUser, font=fontUser)
    # setting position

    userX = (IMAGE_WIDTH - text_widthUser) // 2
    userY = ((IMAGE_HEIGHT - text_heightUser) // 4) + 35
    draw.text(
        (userX, userY),
        textUser,
        fill=color3,
        font=fontUser
    )

    font = ImageFont.truetype('arial.ttf', 25)
    # Third text
    textScore = f"punteggio: {score}"
    text_widthScore, text_heightScore = draw.textsize(textScore, font=font)
    # Setting position
    xPunteggio = ((IMAGE_WIDTH - text_widthScore) // 2) + 150
    yPunteggio = ((IMAGE_HEIGHT - text_heightScore) // 2)
    draw.text(
        (xPunteggio, yPunteggio),
        textScore,
        fill=color2,
        font=font
    )

    # Fourth text
    textLevel = f"livello: {level}"
    text_widthLevel, text_heightLevel = draw.textsize(textLevel, font=font)
    xLivello = (IMAGE_WIDTH - text_widthLevel) - 25
    yLivello = ((IMAGE_HEIGHT - text_heightLevel) // 4)
    draw.text(
        (xLivello, yLivello),
        textLevel,
        fill=color1,
        font=font
    )

    # Saving image
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Sending image
    await message.edit(attachments=[File(buffer, 'rank.png')])