from commands.command import Command
from typing import Optional
from discord import interactions, File
from commands.Images.generate import *
command = Command("poop", "poop")

IMAGE_WIDTH = 500
IMAGE_HEIGHT = 600
AVATAR_SIZE = 128

@command.func
async def poop(
        interaction: interactions.Interaction,
        user: Optional[User] = None
):
    if user is None:
        user = interaction.user
    await interaction.response.defer()
    image = getBasic("./images/calpestato.jpg", (IMAGE_WIDTH, IMAGE_HEIGHT))

    # User
    avatar_image = await getAvatar(user, AVATAR_SIZE)

    # Setting position
    posX = ((IMAGE_WIDTH - AVATAR_SIZE) // 2) - 25
    posY = ((IMAGE_HEIGHT - AVATAR_SIZE) // 1) - 75

    image.paste(
        avatar_image,
        (posX, posY),
        roundAvatar(AVATAR_SIZE)
    )

    # Getting image's buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    # Sending buffer
    message = await interaction.original_response()
    await message.edit(attachments=[File(buffer, 'poop.png')])