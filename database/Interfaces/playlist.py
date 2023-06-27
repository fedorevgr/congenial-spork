from database.Classes.Classes import Playlist
from database.controller import *


class Interface:
    def __init__(self):
        pass

    @staticmethod
    async def createPlaylist(self, name):
        await createTable(name=name)

    @staticmethod
    async def addSong(self, name: str, url: str, duration: int):
        pass

    @staticmethod
    async def deleteSong(self, name: str, url: str, duration: int):
        pass

    @staticmethod
    async def skipSong(self):
        pass

    @staticmethod
    async def previousSong(self):
        pass

    @staticmethod
    async def getPlaylist(self, name: str):
        pass

