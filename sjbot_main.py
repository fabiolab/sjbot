import os
import sys

from discord.ext import commands
from sjbot.ffbad_api import FFBadApi
from loguru import logger

BOT_PREFIX = '$'

bot = commands.Bot(command_prefix=BOT_PREFIX)
api_client = FFBadApi()


@bot.command()
async def alive(ctx):
    logger.info("Is alive !")
    await ctx.send("Yes !")


@bot.command()
async def hello(ctx):
    logger.info("Saying hello")
    await ctx.send('''
    Hello ! Je suis le bot SJB

    Je sais pas faire grand chose mais tu peux m'utiliser pour avoir des infos sur un joueur ou le top du sjb.
    ```
    $info "un numero de licence"
    $top "sh" ou !top "sd" ou !top "dd" ...
    ```
    ''')


@bot.command()
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


@bot.command()
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
        - Simple : :{player_rank.get('simpleSubLevel')}: (best : {player_rank.get('bestSimpleSubLevel')}) - {player_rank.get('simpleRate')} points
        - Double : :{player_rank.get('doubleSubLevel')}: (best : {player_rank.get('bestDoubleSubLevel')}) - {player_rank.get('doubleRate')} points
        - Mixte : :{player_rank.get('mixteSubLevel')}: (best : {player_rank.get('bestMixteSubLevel')}) - {player_rank.get('mixteRate')} points
    
    '''
    await ctx.send(response)


if __name__ == '__main__':
    if not os.getenv('BOT_TOKEN'):
        logger.error("No token found for discord bot. Check your env variables and set 'BOT_TOKEN'")
        sys.exit(1)

    bot_token = os.getenv('BOT_TOKEN')
    logger.info("Running the bot ...")
    bot.run(bot_token)
