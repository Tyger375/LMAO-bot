from discord import Embed, Color, User
def Errore(author: User, errore) -> Embed:
    return Embed(
        color=Color.dark_red(),
        description=f"<a:error:892766709755301938> {errore}"
    )\
    .set_author(
        icon_url=author.display_avatar.url,
        name=f"[Errore] {author.name}"
    )