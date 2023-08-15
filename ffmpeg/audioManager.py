import os
from time import time
import logging


offsetTime = 60 * 60
logger = logging.getLogger("discord")


def clearCache():
    listOfFiles = os.listdir(path='/'.join(os.getcwd().split('\\')) + '/ffmpeg/audio')
    for soundtrack in listOfFiles:
        if time() - os.path.getctime('/'.join(os.getcwd().split('\\')) + '/ffmpeg/audio'+f"/{soundtrack}") > offsetTime:
            os.remove(f"ffmpeg/audio/{soundtrack}")
            logger.info(f"Removed ffmpeg/audio/{soundtrack}")
    logger.info(f"Cleanup finished...")
