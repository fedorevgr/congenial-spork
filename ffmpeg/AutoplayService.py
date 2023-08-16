from g4f import ChatCompletion
import database.Classes.Classes as Classes
from tools import tools
from ffmpeg import downloader


class AutoplayService:
    def __init__(self):
        self.__autoPLayIsON = False

    def setAutoplay(self):
        self.__autoPLayIsON  = not self.__autoPLayIsON

    def getAutoplayMode(self):
        return self.__autoPLayIsON

    @classmethod
    def __prompt(cls, baseMelody: Classes.Song):
        return f"Compose a list of 10 song," \
               f" which are similar to {baseMelody.name}," \
               f"they have to share same tones, emotions and etc."

    def composeList(self, baseMelody: Classes.Song) -> list[Classes.Song]:
        response = ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": self.__prompt(baseMelody)}],
            stream=True
        )
        response = [
            songName[songName.find('"')+1:songName.rfind('"')]
            for songName in "".join(response).split("\n")
            if '"' in songName
        ]
        outputList = []
        for songName in response:
            if '"' in songName:
                songName = songName[songName.find('"')+1:songName.rfind('"')]
                songName, songURL = tools.assignNameUrl(songName)
                songFilename, songDuration = await downloader.YTDLSource.from_url(songURL), tools.getDuration(songURL)
                song = Classes.Song(name=songName, duration=songDuration, url=songURL, systemName=songFilename)

                outputList.append(song)
        return outputList
