from database.Classes.Classes import Queue, Song
from ffmpeg.downloader import YTDLSource
# no controller, because after the shut-down queue is no longer needed


class Interface(Queue):
    def addSong(self, name: str, url: str, duration: 0, systemName: str):
        self.append(Song(name=name, url=url, duration=duration, systemName=systemName))

    async def deleteSong(self, name: str):
        self.pop([i for i, song in enumerate(self) if song.name == name][0])

    async def skipSong(self):
        return self.pop(0)

    async def previousSong(self):
        pass

    def get(self):
        return "\n".join(f'{i+1} - "{song.name.capitalize()}" ({song.duration//60}:{song.duration%60})'
                         for i, song in enumerate(self))
