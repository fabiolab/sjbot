import os

import discord
from loguru import logger


class SjbotClient(discord.Client):
    async def on_ready(self):
        logger.info('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'info':
            await message.channel.send(f"{message.author} / {message.author.name}")
        else:
            await message.channel.send(
                f'Hey {message.author}! Work in progress. Soon, I will be able to send Strava activities for SJB in the cap channel !')


if __name__ == '__main__':
    bot_token = os.getenv('BOT_TOKEN')
    client = SjbotClient()
    client.run(bot_token)
