from commands.command import Command
from typing import Optional
from discord import interactions, File
from commands.Images.generate import *
from PIL import ImageOps, ImageFont
import random
command = Command("wanted", "wanted")

IMAGE_WIDTH = 500
IMAGE_HEIGHT = 600
AVATAR_SIZE = 256

@command.func
async def Wanted(
    interaction: interactions.Interaction,
    user: Optional[User]=None
):
    if user is None:
        user = interaction.user
    await interaction.response.defer()

    cash = random.randint(1, 10)

    img = getBasic("images/wanted.jpg", (IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(img)

    # Getting user's avatar
    avatar_image = await getAvatar(user, AVATAR_SIZE)
    avatar_image = ImageOps.expand(avatar_image, border=25)

    # Setting position
    posX = (IMAGE_WIDTH - (AVATAR_SIZE + 25)) // 2
    posY = (IMAGE_HEIGHT - (AVATAR_SIZE + 25)) // 2

    img.paste(avatar_image, (posX, posY))

    # Adding text
    text = f"${cash}000 reward"
    font = ImageFont.truetype('arial.ttf', 70)
    text_width, text_height = draw.textsize(text, font=font)

    # Setting position
    x = (IMAGE_WIDTH - text_width) // 2
    y = ((IMAGE_HEIGHT - text_height) // 1) - 25

    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # Saving image
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Sending image
    message = await interaction.original_response()
    await message.edit(attachments=[File(buffer, 'wanted.png')])