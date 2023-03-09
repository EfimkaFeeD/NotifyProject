import yandex_music
from telegram.utils import config


conn = yandex_music.Client(token=config.MUSIC_TOKEN)
conn.init()


def search(query):
    response = []
    answer = conn.search(text=query, type_='track')
    for item in answer[:10]:
        response.append({"id": item.id, "name": item.title, "artists": ", ".join([i.name for i in item.artists])})


def get_link(track_id):
    track = yandex_music.Track(id=track_id, client=conn)
    track.get_download_info()
    return track.download_info[0].get_direct_link()
