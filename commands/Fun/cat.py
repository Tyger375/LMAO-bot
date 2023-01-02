from commands.command import Command
from discord import interactions
import random
import requests
command = Command("cat", "cat")

@command.func
async def Cat(interaction: interactions.Interaction):
    await interaction.response.defer()
    req = requests.get(f'https://www.reddit.com/r/cat/best/.json', headers={
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "discord-feed-bot"
    })
    posts = req.json()['data']['children']
    qualeMeme = random.randint(0, len(posts) - 1)
    post = posts[qualeMeme]
    message = await interaction.original_response()
    await message.edit(content=post["data"]["url"])
