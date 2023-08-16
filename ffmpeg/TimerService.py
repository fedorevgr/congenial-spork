import asyncio


class Timer:
    def __init__(self, endPlay=False):
        self._elapsed = 0
        self._isPaused = False
        self._isSkipped = False
        self._delay = 0.5
        self._duration = 0
        self._endlessPlay = endPlay

    def switchEndless(self):
        self._endlessPlay = not self._endlessPlay
        return self._endlessPlay

    def getEndless(self):
        return self._endlessPlay

    def switchPause(self):
        self._isPaused = not self._isPaused
        return self._isPaused

    def switchSkip(self):
        self._isSkipped = not self._isSkipped

    async def startTimer(self, duration):
        self._duration, self._elapsed = duration, 0
        while self._duration + 2 > self._elapsed:
            await asyncio.sleep(self._delay)
            if self._isPaused:
                continue
            if self._isSkipped:
                self._endlessPlay = False
                break
            self._elapsed += self._delay
        self.__init__(self._endlessPlay)
        return

    def time(self):
        return int(self._elapsed),  self._duration
