import aiosqlite


class Commands:
    def createTable(self, name, properties):
        return f"CREATE TABLE {name}({', '.join(properties)})"


class DataBase:
    def __init__(self):
        self.base = await aiosqlite.connect("botDatabase.db")
        self.commands = Commands()

    async def create(self):
        await self.base.execute(self.commands.createTable("queue", []))
