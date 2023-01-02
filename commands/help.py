from typing import Literal, Optional

from commands.command import Command
from discord import interactions, Embed, Color
command = Command("help", "Help command")

def build(cmds: dict[str, str]) -> str:
    return "".join([f"{Arrow} `/{cmd}` - {desc}\n" for cmd, desc in cmds.items()])[:-1]
Arrow = "<a:lmao_arrow:900727528694632469>"

fun = build({
    "barzelletta": "Il bot ti racconta una barzelletta *divertente*",
    "indovinello": "Il bot ti fa un indovinello *divertente*",
    "aiutami": "Ti aiuta a prendere le decisioni",
    "cat": "Ti mostra una foto di un gattino",
    "love": "Indice di <3 tra te e l'utente menzionato",
    "info": "Usalo per sapere le *vere* info di un account discord",
    "insieme": "Guarda youtube o gioca a scacchi insieme ai tuoi amici!"
})

altro = build({
    "image": "Usalo per visualizzare l'immagine del profilo di qualcuno",
    "consiglio": "Scrivi il tuo consiglio, verrà preso in considerazione",
    "partner": "Ti da la lista dei server partner",
    "invito": "Ti manda il link per invitare il bot nel tuo server",
    "bot-info": "Ti manda le info del bot",
    "vote-bot": "Ti manda il link per votare il bot",
    "donate": "Ti piace Lmao bot? Puoi supportare tyger 375#4141 donando su paypal"
})

minigames = build({
    "giochiamo": "Gioca con il bot a vari minigiochi",
    "scommetto": "Prova ad indovinare il numero!",
    "ttt": "Gioca a tic tac toe",
    "duel-user": "Sfida un'altra persona a chi scrive per primo una frase"
})

meme = build({
    "wanted": "",
    "shit": "",
    "well": "",
    "stonks": "",
    "bruh": "",
    "boom": "",
    "hecker": "",
    "delete": ""
})

economy = build({
    "daily": "Riscatta i tuoi punti Lmao bot giornalieri",
    "ruba": "Ruba punti Lmao Bot a qualcuno",
    "rank": "Usalo per sapere il tuo livello e il tuo punteggio",
    "ranks": "Usalo per vedere i primi 5 utenti con il punteggio maggiore"
})

params = {
    "fun": ("Fun", fun),
    "altro": ("Altro", altro),
    "minigames": ("Minigiochi", minigames),
    "meme":
        Embed(title="Comandi meme")
        .add_field(
            name=f"{Arrow} `/meme`",
            value="Ti manda un meme tra i top delle 24 ore nel subreddit memesITA"
        )
        .add_field(
            name="Foto edits",
            value=meme,
            inline=False
        ),
    "codici":
        Embed(title="❓ Domande frequenti sui codici LMAO bot ❓")
        .add_field(
            name="Cosa sono codici LMAO bot?",
            value="I codici LMAO bot sono dei codici che possono essere riscattati per ottenere dei premi esclusivi",
            inline=False
        )
        .add_field(
            name="Ho un codice LMAO bot, come posso riscattarlo?",
            value="Per riscattare un codice LMAO bot, vai sul sito: https://lmaobot.gq/Codici/Codici fai il login con il tuo account discord ed inserisci il tuo codice (ricordati che per riscattarlo devi aver fatto almeno una partita ad un minigioco LMAO bot)",
            inline=False
        )
        .add_field(
            name="Come posso ottenere un codice LMAO bot?",
            value="I codici LMAO bot si possono ottenere tramite giveaway, li puoi trovare nel server di supporto, oppure in alcuni server partner con il bot",
            inline=False
        ),
    "economy": ("Economy", economy)
}

@command.func
async def help_command(
        interaction: interactions.Interaction,
        type: Optional[Literal[tuple(params.keys())]]
):
    if type is None:
        Folder = "<:lmao_folder:900723654999040050>"
        Links = "<:lmao_links:901433510668169256>"
        embed = Embed(title="Comandi Bot")
        categorie1 = """
            > **Minigames**
            > **Fun**
            > **Meme**
            """
        categories2 = """
            > **Altro**
            > **Codici**
            > **Economy**
            """
        # Links
        invite = "https://discord.com/oauth2/authorize?client_id=856159162466304040&permissions=2147875904&scope=bot%20applications.commands"
        website = "https://lmaobot.gq"
        supportServer = "https://discord.gg/WVKC8kktEx"
        topGG = "https://top.gg/bot/856159162466304040"

        LinksEmbed = f"""
            > [**Invita**]({invite})
            > [**Sito**]({website})
            > [**Server Supporto**]({supportServer})
            > [**Top gg**]({topGG})
            """
        embed\
        .add_field(name=Folder + " Categorie", value=categorie1, inline=True)\
        .add_field(name="\u200b", value=categories2, inline=True)\
        .add_field(name=Links + " Links", value=LinksEmbed, inline=False)
    else:
        typeTuple = params[type]
        if type(typeTuple) == tuple:
            embed = Embed(title=typeTuple[0]).add_field(name="Comandi", value=typeTuple[1])
        else:
            embed = typeTuple
    embed.color = Color.gold()
    await interaction.response.send_message(content="Help Command!", embed=embed)
