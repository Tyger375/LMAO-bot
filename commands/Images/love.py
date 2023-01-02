from commands.command import Command
from discord import interactions, File
from commands.Images.generate import *
import io
import random
from PIL import Image, ImageDraw, ImageFont
command = Command("love", "love")

AVATAR_SIZE = 128
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 300

@command.func
async def love(
        interaction: interactions.Interaction,
        user: User
):
    await interaction.response.defer()
    img: Image = getBasic("images/sfondo.jpg", (IMAGE_WIDTH, IMAGE_HEIGHT))

    draw = ImageDraw.Draw(img)
    circle_image = roundAvatar(AVATAR_SIZE)

    # First user
    # Getting avatar
    avatar_image = await getAvatar(interaction.user, AVATAR_SIZE)

    # Setting position
    posX = (IMAGE_WIDTH - AVATAR_SIZE) // 10
    posY = (IMAGE_HEIGHT - AVATAR_SIZE) // 2

    img.paste(avatar_image, (posX, posY), circle_image)

    # Second user (mentioned)
    avatar_image2 = await getAvatar(user, AVATAR_SIZE)

    # Setting position
    posX2 = ((IMAGE_WIDTH - AVATAR_SIZE) // 1) - 25
    posY2 = (IMAGE_HEIGHT - AVATAR_SIZE) // 2

    img.paste(avatar_image2, (posX2, posY2), circle_image)

    # Adding text
    text = f"{random.randint(0,100)}%"

    # Importing font
    font = ImageFont.truetype('arial.ttf', 55)
    text_width, text_height = draw.textsize(text, font=font)

    # Setting position
    textX = (IMAGE_WIDTH - text_width) // 2
    textY = (IMAGE_HEIGHT - text_height) // 2

    draw.text(
        (textX, textY),
        text,
        fill=(0, 0, 255),
        font=font
    )

    # Getting image's buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Sending image
    message = await interaction.original_response()
    await message.edit(attachments=[File(buffer, 'love.png')])
