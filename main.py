import logging
import os
import sys

from tools.info import *

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
    for elem in commands.values():
        os.system(f"pip install {elem}")
    mainLogger.info("Everything should work")

