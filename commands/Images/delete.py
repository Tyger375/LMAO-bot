from commands.command import Command
from typing import Optional
from discord import interactions, File
from commands.Images.generate import *
command = Command("delete", "delete")

IMAGE_WIDTH = 950
IMAGE_HEIGHT = 450
AVATAR_SIZE = 256

@command.func
async def DeleteCmd(
    interaction: interactions.Interaction,
    user: Optional[User]
):
    if user is None:
        user = interaction.user
    await interaction.response.defer()
    img = getBasic("./images/delete.png", (IMAGE_WIDTH, IMAGE_HEIGHT))

    # Getting avatar
    avatar_image = await getAvatar(user, AVATAR_SIZE)

    # Setting position
    posX = ((IMAGE_WIDTH - AVATAR_SIZE) // 4) - 21
    posY = ((IMAGE_HEIGHT - AVATAR_SIZE) // 2) + 70

    img.paste(avatar_image, (posX, posY))

    # Saving image
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Sending image
    message = await interaction.original_response()
    await message.edit(attachments=[File(buffer, 'delete.png')])