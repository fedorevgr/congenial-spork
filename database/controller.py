import aiosqlite

#  db scheme queue; playlists playlist.{name}(songName, url, duration)


__filename = "botDatabase.db"


async def f(command: str) -> None:
    __database = await aiosqlite.connect(__filename)
    await __database.execute(command)
    await __database.close()


async def insert(where: str, what: str):
    await f("INSERT")


async def remove(where: str, what: str):
    pass


async def createTable(name: str, *params):
    await f(f"create table {name}({', '.join(params)})")
    return getTable(name)


async def getTable(name: str):
    pass

async def getRow(what: str):
    pass


async def getColumn(where: str, what: str):
    pass


async def resetDatabase(keepPlaylists: bool) -> None:
    pass