from g4f import ChatCompletion
from g4f import Provider
import database.Classes.Classes as Classes
import database.Interfaces.queue as queue
from TOOLS import tools
from ffmpeg import downloader
import asyncio
import TOOLS.messagesService as systemMessages


class AutoplayService:
    def __init__(self):
        self.__autoPLayIsON = False

    def setAutoplayMode(self, mode):
        self.__autoPLayIsON = mode

    def getAutoplayMode(self):
        return self.__autoPLayIsON

    @classmethod
    def __prompt(cls, baseMelody):
        return f"Compose a list of 10 song," \
            f" which are similar {baseMelody}" \
            f"they have to share same tones, emotions and etc." \
            f"They don't have to be only from one specific band, author, singer. " \
            f"Show me a list in this form: position name -  author."

    def getResponse(self, name):
        response = "".join(ChatCompletion.create(
            model='gpt-3.5-turbo',
            provider=Provider.GetGpt,
            messages=[{"role": "user", "content": self.__prompt(name)}],
            stream=True
        ))
        return response

    async def AutoplayToQueue(self, songQueue: queue.Interface, message=None):
        for i in range(30):
            RAWResponse = self.getResponse(name=songQueue[0].name)
            systemMessages.onRawResponse("".join(RAWResponse))
            if RAWResponse:
                break
            await asyncio.sleep(1)

        if RAWResponse == "":
            self.__autoPLayIsON = False
            return
        else:

            index = 1
            for line in RAWResponse.split("\n"):
                name = line[line.find(".")+2:]
                name, url = tools.assignNameUrl(name)
                duration, filename = tools.getDuration(url), await downloader.YTDLSource.from_url(url=url)
                songQueue.addSong(name=name, url=url, duration=duration, systemName=filename, index=index)
                index += 1
            self.__autoPLayIsON = True

            return songQueue

    def cleanUp(self):
        self.__init__()
