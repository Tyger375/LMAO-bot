import random
import discord
from discord import Embed, Color
from discord.interactions import Interaction
from discord.ui import Button, View
from commands.Minigames.result import Win, Lose

waiting = "in attesa..."
waitingPlayer = "in attesa del giocatore..."
moves = {
    "sasso": "🪨",
    "carta": "📰",
    "forbice": "✂️"
}
final = {
    "sasso": {
        "carta":"perso",
        "forbice":"vinto"
    },
    "carta": {
        "forbice": "perso",
        "sasso": "vinto"
    },
    "forbice": {
        "sasso": "perso",
        "carta": "vinto"
    }
}

class Buttons(View):
    def __init__(self, rps):
        super().__init__()
        self.rps: RPS = rps

    async def btnClicked(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.rps._interaction.user.id:
            return await interaction.response.send_message(content="Non hai il permesso", ephemeral=True)
        for child in self.children:
            child.disabled = True
        self.rps.setPlayerMove(button.label)
        await self.rps.end()
        await interaction.response.edit_message(embed=self.rps.embed, view=self.rps.components)


    @discord.ui.button(label="sasso", emoji="🪨")
    async def rock(self, interaction: Interaction, button: Button):
        await self.btnClicked(interaction, button)

    @discord.ui.button(label="carta", emoji="📰")
    async def paper(self, interaction: Interaction, button: Button):
        await self.btnClicked(interaction, button)

    @discord.ui.button(label="forbice", emoji="✂️")
    async def scissor(self, interaction: Interaction, button: Button):
        await self.btnClicked(interaction, button)

class RPS:
    def __init__(self, interaction):
        # moves
        self.player = waiting
        self.bot = waitingPlayer
        # stats
        self.result = "Stanno ancora giocando"
        self.playing = True
        # discord message
        self.embed = self._buildEmbed()
        self.components = Buttons(self)
        self._interaction: Interaction = interaction

    async def end(self):
        if not self.player in moves.keys():
            return
        self.bot = list(moves.keys())[random.randint(0, 2)]

        m1 = self.player
        m2 = self.bot
        if m1 == m2:
            self.result = "Pareggio!"
        else:
            self.result = final[m1][m2]
            client = self._interaction.client
            userId = self._interaction.user.id
            if self.result == "vinto":
                await Win(client, userId)
            elif self.result == "perso":
                await Lose(client, userId)
            self.result = f"{self._interaction.user.name} ha {self.result}!"
        self.embed = self._buildEmbed()

    def setPlayerMove(self, move: str):
        self.player = move

    def _buildEmbed(self) -> Embed:
        return Embed(title="Sasso carta forbice", color=Color.dark_gold()) \
            .add_field(name="Mossa giocatore", value=self.player, inline=False) \
            .add_field(name="Mossa bot", value=self.bot, inline=False) \
            .add_field(name="Risultato", value=self.result, inline=False)

    async def send(self):
        await self._interaction.response.send_message(embed=self.embed, view=self.components)

async def SCF(interaction: Interaction):
    game = RPS(interaction)
    await game.send()