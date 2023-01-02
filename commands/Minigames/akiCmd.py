import datetime
import discord.ui
from discord.interactions import Interaction
from discord.ui import View, Button
from discord import User, Embed, Color, ButtonStyle
import akinator

moves = {
    "Si": "Yes",
    "No": "No",
    "Non lo so": "Idk",
    "Probabilmente": "Probably",
    "Probabilmente no": "Probably not",
    "Indietro": "b"
}

class Buttons(View):
    def __init__(self, akiGame):
        super().__init__()
        self.akiGame: AkiGame = akiGame

    @discord.ui.button(label="Si", row=0, style=ButtonStyle.green)
    async def Yes(self, interaction: Interaction, button: Button):
        await self.akiGame.answer(interaction, button)

    @discord.ui.button(label="No", row=0, style=ButtonStyle.red)
    async def No(self, interaction: Interaction, button: Button):
        await self.akiGame.answer(interaction, button)

    @discord.ui.button(label="Non lo so", row=0)
    async def Idk(self, interaction: Interaction, button: Button):
        await self.akiGame.answer(interaction, button)

    @discord.ui.button(label="Probabilmente", row=0)
    async def Probably(self, interaction: Interaction, button: Button):
        await self.akiGame.answer(interaction, button)

    @discord.ui.button(label="Probabilmente no", row=0)
    async def ProbablyNot(self, interaction: Interaction, button: Button):
        await self.akiGame.answer(interaction, button)

    @discord.ui.button(label="Indietro", row=1)
    async def Return(self, interaction: Interaction, button: Button):
        await self.akiGame.answer(interaction, button)

    @discord.ui.button(label="End game", row=1)
    async def EndGame(self, interaction: Interaction, button: Button):
        if interaction.user.id != self.akiGame._interaction.user.id:
            return await interaction.response.send_message(content="Non hai il permesso", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            embed=Embed(
                title="Akinator",
                color=discord.Color.dark_green()
            )\
            .add_field(
                name="Partita terminata",
                value=f"{interaction.user.name} ha terminato la partita"
            ),
            view=self
        )

class ButtonsVerificaPersonaggio(View):
    def __init__(self, firstInteraction: Interaction):
        super().__init__()
        self._firstInteraction = firstInteraction
    async def btnClicked(self, interaction):
        if interaction.user.id != self._firstInteraction.user.id:
            return await interaction.response.send_message(content="Non hai il permesso", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Si")
    async def Si(self, interaction: Interaction, button: Button):
        if interaction.user.id != self._firstInteraction.user.id:
            return await interaction.response.send_message(content="Non hai il permesso", ephemeral=True)
        await self.btnClicked(interaction)
        await interaction.channel.send("Yay!")

    @discord.ui.button(label="No")
    async def No(self, interaction: Interaction, button: Button):
        await self.btnClicked(interaction)
        await interaction.channel.send("Oof!")

class AkiGame:
    def __init__(self, interaction: Interaction):
        self.game = akinator.Akinator()
        self.q = self.game.start_game(language="it")
        self.lastInteraction: datetime.datetime = datetime.datetime.now()
        self._interaction: Interaction = interaction
        self.player: User = interaction.user
        self.embed = self._buildEmbed()
        self.buttons = Buttons(self)

    def _buildEmbed(self) -> Embed:
        return Embed(title="Akinator", color=Color.dark_green()).add_field(name="Domanda", value=self.q)

    async def send(self):
        await self._interaction.response.send_message(embed=self.embed, view=self.buttons)

    async def edit(self, interaction: Interaction):
        self.embed = self._buildEmbed()
        await interaction.response.edit_message(embed=self.embed, view=self.buttons)

    async def answer(self, interaction: Interaction, button: Button):
        if interaction.user.id != self._interaction.user.id:
            return await interaction.response.send_message(content="Non hai il permesso", ephemeral=True)
        if self.game.progression <= 80:
            label = button.label
            if label == "End game":
                return

            self.lastInteraction = datetime.datetime.now()
            move = moves[label]
            if move == "b":
                try:
                    self.q = self.game.back()
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                self.q = self.game.answer(move)
            await self.edit(interaction)
        else:
            self.game.win()
            print(self.game.first_guess)
            self.embed = Embed(title="Akinator", color=discord.Color.dark_green())\
            .add_field(
                name=f"È {self.game.first_guess['name']}?",
                value=self.game.first_guess["description"]
            )\
            .set_thumbnail(
                url=str(self.game.first_guess['absolute_picture_path'])
            )
            await interaction.response.edit_message(
                content="",
                embed=self.embed,
                view=ButtonsVerificaPersonaggio(self._interaction)
            )


async def Aki(interaction: Interaction):
    game = AkiGame(interaction)
    await game.send()
