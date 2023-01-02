import random
from discord.interactions import InteractionResponse

futuro1 = [
    "Mangierai un gelato",
    "Ti allaccierai le scarpe",
    "Mangierai",
    "Correrai",
    "Andrai a scuola"
]
futuro2 = [
    "saltando su due piedi",
    "in ginocchio",
    "in pigiama",
    "dormendo",
]

async def future(interaction: InteractionResponse):
    randomFuture1 = random.randint(0, len(futuro1) - 1)
    randomFuture2 = random.randint(0, len(futuro2) - 1)
    message = f"{futuro1[randomFuture1]} {futuro2[randomFuture2]}"
    await interaction.send_message(message)