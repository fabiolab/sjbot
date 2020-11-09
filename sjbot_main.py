import os
import sys
import discord
from discord.ext import commands
from sjbot.ffbad_api import FFBadApi
from loguru import logger

BOT_PREFIX = '$'
RANKS_EMOJII = {
    "R6": "<:R6:710586107560984680>",
    "R5": "<:R5:710586107737276537>",
    "R4": "<:R4:710586107426766889>",
    "P12": "<:P12:710583882776576161>",
    "P11": "<:P11:710586107397406720>",
    "P10": "<:P10:710586107124908043>",
    "NC": "<:NC:710586107724824617>",
    "N3": "<:N3:710586107477098587>",
    "N2": "<:N2:710586107703853087>",
    "N1": "<:N1:710586107653259324>",
    "D9": "<:D9:710586107561115669>",
    "D8": "<:D8:710586107712241765>",
    "D7": "<:D7:710586107389018195>",
}

bot = commands.Bot(command_prefix=BOT_PREFIX)
api_client = FFBadApi()

bot.remove_command("help")


# @bot.event
# async def on_message(message):
#     # Direct dialog with the bot
#     if "hello" in message.content.lower().split():
#         await message.channel.send("Hello ! Bon, je sais dire que ça en fait.")
#     else:
#         await message.channel.send("Nan, mais je pige rien. Que 'hello', et encore.")
#
#     # Necessary to make on_message work with commands
#     await bot.process_commands(message)
#

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help",
                       description=f"Utilise {BOT_PREFIX}<commande> pour interroger SJBot",
                       color=discord.Colour.dark_orange())
    em.add_field(name="Information", value="info, top")
    em.add_field(name="Misc", value="alive, hello")
    await ctx.send(embed=em)


@bot.command(
    help="Est-ce que le bot est vivant ?"
)
async def alive(ctx):
    logger.info("Is alive !")
    await ctx.send("Yes !")


@bot.command(
    help="Dis bonjour au robot"
)
async def hello(ctx):
    logger.info("Saying hello")
    await ctx.send('''
Hello ! Je suis le bot SJB

Je sais pas faire grand chose mais tu peux m'utiliser pour avoir des infos sur un joueur ou le top du sjb.
```
$info "un numero de licence"
$top "sh" ou $top "sd" ou $top "dd" ...
```
''')


@bot.command(
    help="Donne les tops joueurs du club.\n `$top sh` - $top sd - $top dd - $top dm - $top dh"
)
async def top(ctx, discipline: str):
    top_players = api_client.get_club_top(discipline)

    logger.info(top_players[:5])
    response = f'\n**TOP 20 Sjb en {discipline.upper()} !**\n'
    if not top_players:
        response += "Aucun joueur"
        top_players = []

    for player in top_players[:20]:
        response += f'{player.get("rank")}. {player.get("name")} ({player.get("subLevel")} - nat : {player.get("frenchRank")})\n'

    await ctx.send(response)


@bot.command(
    help="Donne toutes les infos possibles sur un joueur.\n $info numero_licence"
)
async def info(ctx, licence: str):
    logger.info(f"Getting info for {licence}")
    player_info = api_client.get_player_info(licence)
    if not player_info:
        response = f"Aucun joueur trouvé pour la licence {licence}"
    else:
        player_rank = api_client.get_player_ranking(player_info.get('personId'), licence)
        response = f'''

    Voilà tout ce que je sais sur la licence **{licence}**

    **{player_info.get('firstName')} {player_info.get('lastName')}** ({player_info.get('player').get('category')})
        - Simple : {transform_rank(player_rank.get('simpleSubLevel'))} (best : {transform_rank(player_rank.get('bestSimpleSubLevel'))}) - {player_rank.get('simpleRate')} points
        - Double : {transform_rank(player_rank.get('doubleSubLevel'))} (best : {transform_rank(player_rank.get('bestDoubleSubLevel'))}) - {player_rank.get('doubleRate')} points
        - Mixte : {transform_rank(player_rank.get('mixteSubLevel'))} (best : {transform_rank(player_rank.get('bestMixteSubLevel'))}) - {player_rank.get('mixteRate')} points

    '''
    await ctx.send(response)


def transform_rank(rank: str) -> str:
    return RANKS_EMOJII.get(rank.upper(), rank)


if __name__ == '__main__':
    if not os.getenv('BOT_TOKEN'):
        logger.error("No token found for discord bot. Check your env variables and set 'BOT_TOKEN'")
        sys.exit(1)

    bot_token = os.getenv('BOT_TOKEN')
    logger.info("Running the bot ...")
    bot.run(bot_token)
