from youtubesearchpython import VideosSearch


def assignNameReps(args):
    repeat = 0
    if args[-1].startswith("repeat="):
        args, repeat = args[:-1], int(args[-1][7:])
    elif args[-1].startswith("r="):
        args, repeat = args[:-1], int(args[-1][2:])
    songName = " ".join(args)
    return songName, repeat


def assignNameUrl(url_name):
    url = url_name
    if not url_name.startswith("https"):
        name = url_name
        url, name = __getUrl(url_name), __getName(url_name)
    else:
        name = __getName(url_name)
    return name, url


def __getUrl(fromName: str):
    videosSearch = VideosSearch(fromName, limit=1)
    video_info = videosSearch.result()
    video_url = video_info['result'][0]['link']
    return video_url


def __getName(fromUrl):
    videoSearch = VideosSearch(fromUrl, limit=1)
    videoInfo = videoSearch.result()
    return videoInfo["result"][0]["title"]

def getDuration(fromUrl):
    videoSearch = VideosSearch(fromUrl, limit=1)
    videoInfo = videoSearch.result()
    res = videoInfo["result"][0]['duration'].split(":")[::-1]
    return sum([(60**i)*int(value) for i, value in enumerate(res)])


def getThumbnailUrl(url):
    videoSearch = VideosSearch(url, limit=1)
    videoInfo = videoSearch.result()
    return videoInfo["result"][0]['thumbnails'][0]["url"]