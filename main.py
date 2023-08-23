import logging
import os
import sys

from TOOLS.info import *

if __name__ == "__main__":
    mainLogger = logging.getLogger("Main")
    mainLogger.setLevel(logging.INFO)
    if sys.prefix == sys.base_prefix:
        os.system("python3 -m venv venv")
        mainLogger.info("Created venv")
        if sys.platform.startswith("win"):
            os.system(".\venv\Scripts\activate")
        else:
            os.system("source venv/bin/activate")
        mainLogger.info("Activated venv")
    else:
        mainLogger.info(f"venv is active. {sys.platform}")
    for elem in libs.values():
        os.system(f"pip install {elem}")
    if "audio" not in os.listdir("ffmpeg"):
        mainLogger.info(f"Created AUDIO directory in ffmpeg")
        os.mkdir("ffmpeg/audio")
    mainLogger.info("Everything should work")

