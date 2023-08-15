import discord
import logging
import platform
import os
import tools.tools as computations


logger = logging.getLogger("discord")


def logOnStartUp(botName):
    logger.info(f"Logged in as {botName}")
    logger.info(f"discord.py API version: {discord.__version__}")
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    logger.info(f"Working directory: "+ '/'.join(os.getcwd().split('\\')))
    logger.info("-------------------")


async def onAdditionOfSong(msg, name, elem):
    logger.info(f'Song "{name}" is added to queue.')
    message = f"Добавил die Musik -------  {name}  ({elem.duration // 60}:{str(elem.duration % 60).rjust(2, '0')})"
    await msg.reply(message)


async def onCurrSong(msg, elem):
    embed = discord.Embed(
        url=elem.url,
        title=f"Сейчас играет - {elem.name}",
        description=f"{elem.duration // 60}:{str(elem.duration % 60).rjust(2, '0')}",
        colour=discord.Colour.random(),
    )
    embed.set_image(url=computations.getThumbnailUrl(elem.url))
    await msg.channel.send(embed=embed)

