from g4f import ChatCompletion
import database.Classes.Classes as Classes
import database.Interfaces.queue as queue
from tools import tools
from ffmpeg import downloader
import asyncio
import tools.messagesService as systemMessages

class AutoplayService:
    def __init__(self):
        self.__autoPLayIsON = False

    def setAutoplay(self):
        self.__autoPLayIsON = not self.__autoPLayIsON
        return self.__autoPLayIsON

    def getAutoplayMode(self):
        return self.__autoPLayIsON

    @classmethod
    def __prompt(cls, baseMelody: Classes.Song):
        return f"Compose a list of 10 song," \
               f" which are similar to {baseMelody.name}," \
               f"they have to share same tones, emotions and etc. Show me a list in this form: position name -  author"

    async def composeList(self, baseMelody: Classes.Song):

        response = ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{"role": "user", "content": self.__prompt(baseMelody)}],
                    stream=True
                )
        if response:
            outputList = queue.Interface()
            for songName in ("".join(response)).split("\n"):
                if '"' in songName:
                    songName = songName[songName.find('"')+1:songName.rfind('"')]
                    print(songName)
                    songName, songURL = tools.assignNameUrl(songName)
                    songFilename, songDuration = await downloader.YTDLSource.from_url(songURL), tools.getDuration(songURL)

                    outputList.addSong(name=songName, duration=songDuration, url=songURL, systemName=songFilename)
            systemMessages.composedList(outputList)
            return outputList
        else:
            return False
