class Song:
    def __init__(self, name: str, duration: int, url: str, systemName: str):
        self.name = name
        self.duration = duration
        self.url = url
        self.path = systemName


class Queue(list[Song]):
    pass


class Playlist(list[Song]):
    pass


class Playlists(dict[str: Playlist]):
    pass


