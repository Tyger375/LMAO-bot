from commands.command import Command
from typing import Optional
from discord import interactions, File
from commands.Images.generate import *
from PIL import ImageChops, ImageOps
command = Command("triggered", "triggered")

IMAGE_WIDTH = 500
IMAGE_HEIGHT = 600
AVATAR_SIZE = 128

@command.func
async def triggered(
        interaction: interactions.Interaction,
        user: Optional[User] = None
):
    if user is None:
        user = interaction.user
    await interaction.response.defer()

    # Getting avatar
    avatar_asset = user.display_avatar.with_format("png").with_size(AVATAR_SIZE)
    buffer_avatar = io.BytesIO()
    await avatar_asset.save(buffer_avatar)
    buffer_avatar.seek(0)

    with Image.open(buffer_avatar) as avatar:
        if not avatar:
            return
        offsets = [(15, 15), (5, 10), (-15, -15), (10, -10), (10, 0), (-15, 10), (10, -5)]
        images = []

        red_overlay = Image.new(mode="RGBA", size=avatar.size, color=(255, 0, 0, 255))
        mask = Image.new(mode="RGBA", size=avatar.size, color=(255, 255, 255, 127))
        avatar = Image.composite(avatar, red_overlay, mask)

        # Creating images
        for posX, posY in offsets:
            avatar = avatar.resize((512, 512))
            image = ImageChops.offset(avatar, posX + 15, posY + 15)
            image = ImageOps.crop(image, 15)

            ImageHeight = image.height

            ImageTriggered = Image.open("./images/triggered3.jpg")
            HeightTriggered = ImageTriggered.height

            image.paste(ImageTriggered, (-15 + - (posX // 2), ImageHeight - HeightTriggered + 15 + - (posY // 2)))
            images.append(image)

        avatar = ImageOps.crop(avatar, 15)

        # Saving result as gif
        result = io.BytesIO()
        avatar.save(
            result,
            format="GIF",
            append_images=images,
            save_all=True,
            duration=25,
            loop=0
        )
        result.seek(0)

        # Sending gif
        message = await interaction.original_response()
        await message.edit(attachments=[File(result, 'triggered.gif')])