import discord
from discord import Embed
from discord.colour import Colour
import TOOLS.tools as tools

colours = [
    Colour.red(),
    Colour.orange(),
    Colour.yellow(),
    Colour.green(),
    Colour.blue(),
    Colour.dark_blue(),
    Colour.purple(),
    Colour.gold()
]


class TestEmbed(discord.Embed):
    def __init__(self):
        super().__init__(
            title="Title",
            description="Description",
            colour=0xff0000
        )
        self.set_thumbnail(
            url="https://i.ytimg.com/vi/mUpI0ll9tz4/hq720_live.jpg?sqp=CKCOkqcG-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLBtYjtq0SD4NhTUZ4xNnSTiOhgJlA"
        )
        self.set_footer(
            text="Footer text",
            icon_url="https://yt3.googleusercontent.com/ytc/AOPolaSp8Wwm_MI8F6lM6OyhQdIqPViLXZmg186fOvL0=s176-c-k-c0x00ffffff-no-rj"
        )
        self.set_author(
            name="author name",
            icon_url="https://yt3.googleusercontent.com/ytc/AOPolaSp8Wwm_MI8F6lM6OyhQdIqPViLXZmg186fOvL0=s176-c-k-c0x00ffffff-no-rj"
        )
        self.insert_field_at(
            index=2,
            name="field1name",
            value="field2value"
        )


class ReceiveToQueue(discord.Embed):
    def __init__(self, songName, duration, url):
        super().__init__(title=songName)
        self.set_author(name="Добавил в очередь:")
        self.set_thumbnail(url=tools.getThumbnailUrl(url))
        self.set_footer(text=f"{duration // 60}:{str(duration % 60).rjust(2, '0')}")


class CurrSong(discord.Embed):
    def __init__(self, song):
        super().__init__(title=song.name)
        self.set_author(name="Сейчас играет:")
        self.set_thumbnail(url=tools.getThumbnailUrl(song.url))
        self.set_footer(text=f"{song.duration // 60}:{str(song.duration % 60).rjust(2, '0')}")
