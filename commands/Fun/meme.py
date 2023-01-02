from commands.command import Command
import requests
import random
from discord import interactions
command = Command("meme", "meme")

@command.func
async def gamble(interaction: interactions.Interaction):
    req = requests.get(f'https://www.reddit.com/r/memesITA/top/.json', headers={
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "discord-feed-bot"
    })

    posts = req.json()['data']['children']
    meme = random.randint(0, len(posts) - 1)
    post = posts[meme]
    await interaction.response.send_message(post["data"]["url"])