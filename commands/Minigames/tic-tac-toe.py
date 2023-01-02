from commands.command import Command
from discord import interactions, User, Embed, ButtonStyle, Color
from discord.ui import View, Button, button
command = Command("ttt", "tic-tac-toe")


async def error(content, interaction: interactions.Interaction):
    await interaction.response.send_message(content=content, ephemeral=True)

class Buttons(View):
    def __init__(self, ttt):
        super().__init__()
        self.table = [["-" for _ in range(3)] for _ in range(3)]
        self.ttt: TicTacToe = ttt
        self.first = self.ttt.interaction.user
        self.second = self.ttt.secondPlayer
        self.turn = self.first
        for pos, child in enumerate(self.children):
            child: Button
            if child.label == "End game":
                continue
            x = pos % 3
            y = int(pos/3)
            child.style = ButtonStyle.blurple
            child.custom_id = f"{x},{y}"

    def getEmbed(self):
        return Embed(title=f"{self.first.name} vs {self.second.name}", description=f"E' il turno di {self.turn.name}", color=Color.gold())

    def check(self) -> bool:
        table = self.table

        # Rows
        for y in range(3):
            if table[y][0] == table[y][1] and table[y][1] == table[y][2] and table[y][0] != "-":
                return True

        # Columns
        for x in range(3):
            if table[0][x] == table[1][x] and table[1][x] == table[2][x] and table[0][x] != "-":
                return True

        # Diagonal
        if table[0][0] == table[1][1] and table[1][1] == table[2][2] and table[0][0] != "-":
            return True
        if table[0][2] == table[1][1] and table[1][1] == table[2][0] and table[0][2] != "-":
            return True

        return False

    async def btnClicked(self, interaction: interactions.Interaction, btn: Button):
        userId = interaction.user.id

        if userId not in [self.first.id, self.second.id]:
            return await error("Non hai il permesso", interaction)
        if self.turn.id != userId:
            return await error("Non è il tuo turno", interaction)
        if btn.label != "-":
            return await error("Casella già occupata", interaction)
        char = "X" if interaction.user.id == self.first.id else "O"
        btn.label = char
        btn.style = ButtonStyle.green if char == "X" else ButtonStyle.red

        pos = btn.custom_id.split(",")
        self.table[int(pos[1])][int(pos[0])] = char

        embed: Embed = self.getEmbed()
        if self.check():
            for child in self.children:
                child.disabled = True
            embed.description = f"{self.turn.name} ha vinto!"
            await interaction.response.edit_message(view=self, embed=embed)
        else:
            self.turn = self.first if self.turn.id == self.second.id else self.second
            await interaction.response.edit_message(view=self, embed=self.getEmbed())

    @button(label="-", row=0)
    async def _00(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=0)
    async def _01(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=0)
    async def _02(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=1)
    async def _10(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=1)
    async def _11(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=1)
    async def _12(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=2)
    async def _20(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=2)
    async def _21(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="-", row=2)
    async def _22(self, interaction: interactions.Interaction, btn: Button):
        await self.btnClicked(interaction, btn)

    @button(label="End game", row=3, style=ButtonStyle.gray)
    async def endGame(self, interaction: interactions.Interaction, btn: Button):
        if interaction.user.id not in [self.first.id, self.second.id]:
            return await error("Non hai il permesso", interaction)
        embed = self.getEmbed()
        embed.description = f"{interaction.user.name} ha terminato la partita"
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self, embed=embed)


class TicTacToe:
    def __init__(
        self,
        interaction: interactions.Interaction,
        user: User
    ):
        self.secondPlayer = user
        self.interaction = interaction
        self.view = Buttons(self)

    async def send(self):
        await self.interaction.response.send_message(embed=self.view.getEmbed(), view=self.view)

@command.func
async def tictactoe(
    interaction: interactions.Interaction,
    user: User
):
    ttt = TicTacToe(interaction, user)
    await ttt.send()