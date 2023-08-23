import os

BotURL = "https://discord.com/api/oauth2/authorize?client_id=1108070576733560943&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize&response_type=code&scope=identify%20guilds%20gdm.join%20rpc.voice.read%20rpc.video.write%20rpc.activities.write%20messages.read%20applications.commands%20activities.read%20voice%20applications.commands.permissions.update%20dm_channels.read%20activities.write%20applications.store.update%20applications.builds.upload%20bot%20rpc.screenshare.read%20rpc.voice.write%20rpc%20email%20guilds.join%20connections%20guilds.members.read%20rpc.notifications.read%20rpc.video.read%20rpc.screenshare.write%20webhook.incoming%20applications.builds.read%20applications.entitlements%20relationships.read%20role_connections.write"

DeveloperDiscordId = 426583582920802305

libs = {
    "discord": "discord",
    "yt-dl": "https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz",
    "db": "aiosqlite",
    "help": "pynacl",
    "requests": "requests",
    "yb": "youtube-search-python",
    "gpt": "g4f"
}
gpt = "git clone https://github.com/xtekky/gpt4free"

ffmpegEXEpath = '/'.join(os.getcwd().split('\\')) +"/ffmpeg/ffmpeg.exe"
