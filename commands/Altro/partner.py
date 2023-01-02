from commands.command import Command
from discord import interactions, Embed, Color
command = Command("partner", "partner")

embed = Embed(title="Server partner", color=Color.dark_blue())
partners = {
    "DEMONBLACKTEAM":
        """
        DEMONBLACKTEAM è un gruppo di videogiocatori che si ritrovano insieme per conoscersi, chiacchierare, divertirsi e giocare insieme.
        Il nostro obbiettivo è quello di creare un gruppo di amici che si aiutano a vicenda, cercando di mantenere un clima piacevole.
        <https://discord.gg/DNJjfHJARe>
        """
    ,
    "Jupiter":
        """
        Jupiter è un server progettato per non fare mai finire il divertimento, lo staff cerca di accogliere il più possibile i membri e protegge il server da membri malintenzionati!
        Il nostro server cerca di adattarsi a tutti gli utenti!
        Vogliamo che ti senta come a casa.
        Invito: <https://discord.gg/AbwDsDG2vU>
        """
    ,
    "ł₦₣ł₦ł₮Ɏ ₵ØĐł₦₲":
        """
        ***__ł₦₣ł₦ł₮Ɏ ₵ØĐł₦₲__ :flag_it: :flag_us:***
        > 🏠 Una community in crescita, dedicata alla programmazione e al tempo libero. Il luogo perfetto per incontrarsi e fare nuove amicizie!
        ⧽ 🤝 Partnership.
        ⧽ 🦸 Staff attivo.
        ⧽ 🤖 Tanti bot utili e divertenti.
        ⧽ 🔗 Invito: https://discord.gg/X4nGGPvJJY
        """
    ,
    "The world of programmers":
        """
        The world of programmers server adatto a tutti i programmatori, puoi divertirti parlare con altre persone fare nuove amicizie e lo staff è sempre a disposizione. Troverai tantissimi bot divertenti come <@!856159162466304040>. Bhe che aspetti entra! https://discord.gg/pHfGGduraf
        """
    ,
    "Minecraft Fans [ITA]":
        """
        Sempre in miglioramento
        Staff sempre attivo
        Una community a tema Minecraft
        Che state facendo lì fermi?!
        Dai entrate non ve ne pentirete
        https://discord.gg/cFHMKsWTxx
        """
}
for name, description in partners.items():
    embed.add_field(name=name, value=description, inline=False)
@command.func
async def partner(interaction: interactions.Interaction):
    await interaction.response.send_message(embed=embed)