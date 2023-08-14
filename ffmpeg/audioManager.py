import os
from time import time
import logging


offsetTime = 60 * 60 * 24 * 2
logger = logging.getLogger("discord")


def clearCache():
    listOfFiles = os.listdir(path="ffmpeg/audio")
    for soundtrack in listOfFiles:
        if time() - os.path.getctime(f"ffmpeg/audio/{soundtrack}") > offsetTime:
            os.remove(f"ffmpeg/audio/{soundtrack}")
            logger.info(f"Removed ffmpeg/audio/{soundtrack}")
    logger.info(f"Cleanup finished...")
