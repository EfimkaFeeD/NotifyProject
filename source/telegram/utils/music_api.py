import yandex_music
from telegram.utils import config


conn = yandex_music.Client(token=config.MUSIC_TOKEN)
conn.init()


def search(query):
    track_id = parse_link(query)
    if track_id:
        return [{"id": track_id, "name": get_metadata(track_id)}]
    response = []
    answer = conn.search(text=query, type_='all')
    if not answer.tracks:
        return []
    for item in answer.tracks.results[:10]:
        response.append({"id": item.id, "name": f'{item.title} - {", ".join([i.name for i in item.artists])}'})
    return response


def get_link(track_id):
    return conn.tracks_download_info(track_id=track_id, get_direct_links=True)[0].direct_link


def get_metadata(track_id):
    track = conn.tracks([track_id])[0]
    return f'{track.title} - {", ".join([i.name for i in track.artists])}'


def parse_link(link):
    if not link.startswith('https://music.yandex.ru/'):
        return False
    try:
        re = link.split('/')[6]
        return int(re[:re.index('?')])
    except IndexError and TypeError:
        return False
