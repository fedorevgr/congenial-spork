from database.Classes.Classes import Queue, Song
from ffmpeg.downloader import YTDLSource
# no controller, because after the shut-down queue is no longer needed


class Interface(Queue[Song]):
    async def addSong(self, name: str, url: str, duration: 0, systemName: str):
        await self.put(Song(name=name, url=url, duration=duration, systemName=systemName))

    def getInfo(self):
        return "\n".join(f'{i+1} - "{song.name.capitalize()}" ({song.duration//60}:{song.duration%60})'
                         for i, song in enumerate(self))
