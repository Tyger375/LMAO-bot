from commands.command import Command
from typing import Optional
from discord import interactions, File
from commands.Images.generate import *
command = Command("well", "well")

IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500
AVATAR_SIZE = 256

@command.func
async def well(
        interaction: interactions.Interaction,
        user: Optional[User] = None
):
    if user is None:
        user = interaction.user
    await interaction.response.defer()
    img: Image = getBasic("./images/well.png", (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Getting avatar
    avatar_image = await getAvatar(user, AVATAR_SIZE)

    # Setting position
    posX = ((IMAGE_WIDTH - AVATAR_SIZE) // 2) + 75
    posY = ((IMAGE_HEIGHT - AVATAR_SIZE) // 2) - 25

    img.paste(
        avatar_image,
        (posX, posY),
        roundAvatar(AVATAR_SIZE)
    )

    # Getting image's buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Sending buffer
    message = await interaction.original_response()
    await message.edit(attachments=[File(buffer, 'well.png')])