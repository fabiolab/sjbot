import os
import sys
import discord
from discord.ext import commands, tasks
from sjbot.ffbad_api import FFBadApi
from sjbot.giphy_api import GiphyApi
from sjbot.strava_api import StravaApi
from loguru import logger
from sjbot.bot_messages import BotMessages

BOT_PREFIX = '$'

api_ffbad = FFBadApi()
api_strava = StravaApi()
# api_giphy = GiphyApi(os.getenv('GIPHY_API_KEY'))

bot = commands.Bot(command_prefix=BOT_PREFIX)
bot_messages = BotMessages()

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
                       description=bot_messages.help(BOT_PREFIX),
                       color=discord.Colour.orange())
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
    await ctx.send(bot_messages.hello())


@bot.command(
    help="Donne les tops joueurs du club.\n `$top sh` - $top sd - $top dd - $top dm - $top dh"
)
async def top(ctx, discipline: str):
    top_players = api_ffbad.get_club_top(discipline)

    logger.info(top_players[:5])
    response = bot_messages.top(discipline, top_players)

    await ctx.send(response)


@bot.command(
    help="Donne toutes les infos possibles sur un joueur.\n $info numero_licence"
)
async def info(ctx, licence: str):
    logger.info(f"Getting info for {licence}")
    player_info = api_ffbad.get_player_info(licence)
    if not player_info:
        response = f"Aucun joueur trouvé pour la licence {licence}"
    else:
        player_rank = api_ffbad.get_player_ranking(player_info.get('personId'), licence)
        response = bot_messages.info_player(licence, player_info.get('firstName'), player_info.get('lastName'),
                                            player_info.get('player').get('category'),
                                            player_rank)

    await ctx.send(response)


@tasks.loop(minutes=5.0)
async def check_strava():
    logger.info("cheking strava for new activities")

    last_activities = api_strava.get_activities()

    if not last_activities:
        return

    em = discord.Embed(title=bot_messages.new_strava_activities_title(),
                       description=bot_messages.new_strava_activities(last_activities),
                       color=discord.Colour.orange())

    # em.set_image(url=api_giphy.get_a_gif('run'))
    logger.info(f"sending message to the channel {STRAVA_CHANNEL}")
    channel = await bot.fetch_channel(STRAVA_CHANNEL)
    await channel.send(embed=em)


if __name__ == '__main__':
    if not os.getenv('BOT_TOKEN'):
        logger.error("No token found for discord bot. Check your env variables and set 'BOT_TOKEN'")
        sys.exit(1)

    if not os.getenv('STRAVA_CHANNEL'):
        logger.error("No strava channel for discord bot. Check your env variables and set 'STRAVA_CHANNEL'")
        sys.exit(1)

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    STRAVA_CHANNEL = os.getenv('STRAVA_CHANNEL')

    logger.info("Running the bot ...")
    check_strava.start()
    bot.run(BOT_TOKEN)
