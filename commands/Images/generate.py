from PIL import Image, ImageDraw
from discord import User
import io

def getBasic(filename: str, size: tuple[int, int]):
    img = Image.open(filename)
    img = img.resize(size)
    return img

def roundAvatar(avatar):
    circle_image = Image.new('L', (avatar, avatar))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, avatar, avatar), fill=255)
    return circle_image

async def getAvatar(user: User, size):
    # Getting avatar buffer
    avatar_asset = user.display_avatar.with_format("png").with_size(size)
    buffer_avatar = io.BytesIO()
    await avatar_asset.save(buffer_avatar)
    buffer_avatar.seek(0)

    # avatar into PIL image
    avatar_image = Image.open(buffer_avatar)
    avatar_image = avatar_image.resize((size, size))
    return avatar_image