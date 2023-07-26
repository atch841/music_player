import requests
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
import os
import traceback

from config import DOWNLOAD_STATUS, MUSIC_META, VID_LOOKUP, MUSIC_PATH, DEV_KEY
from config import SONG_URL
from utils import log


def get_music(vid):
    url = f"https://www.youtube.com/watch?v={vid}"
    yt = YouTube(url)
    print(vid + ".mp3")
    _filename = MUSIC_PATH + vid + ".mp3"
    if vid + ".mp3" not in os.listdir(MUSIC_PATH):
        yt.streams.get_audio_only().download(filename=_filename)

def get_vid(song_name):
    if os.path.exists(VID_LOOKUP):
        name_to_vid = json.load(open(VID_LOOKUP, 'r'))
    else:
        name_to_vid = {}

    if song_name in name_to_vid.keys():
        return name_to_vid[song_name]

    with open(DEV_KEY,  'r') as file:
        developerKey = file.read().strip()
    youtube = build('youtube', 'v3', developerKey=developerKey)

    request = youtube.search().list(part="snippet",q=song_name)
    response = request.execute()

    vid = response['items'][0]['id']['videoId']

    name_to_vid[song_name] = vid
    json.dump(name_to_vid, open(VID_LOOKUP, 'w'))

    return vid

def get_song(song_name):
    if os.path.exists(MUSIC_META):
        music_meta = json.load(open(MUSIC_META, 'r'))
    else:
        music_meta = {}

    vid = get_vid(song_name)

    if vid in music_meta.keys():
        return
    get_music(vid)
    music_meta[vid] = {'name': song_name, 'volume': 100}
    json.dump(music_meta, open(MUSIC_META, 'w'))
    

def download_music():
    os.makedirs(os.path.dirname(DOWNLOAD_STATUS), exist_ok=True)

    r = requests.get(SONG_URL)

    song_name = []
    for song in json.loads(r.text)['data']['charts']['newrelease']:
        song_name.append(song['song_name'])

    print('songs:', song_name)

    for idx, song in enumerate(song_name):
        with open(DOWNLOAD_STATUS, 'w') as file:
            file.write(f'{idx}/{len(song_name)}')
        log(f'downloading {song} ({idx}/{len(song_name)})')

        try:
            get_song(song)
        except  Exception:
            log(str(traceback.format_exc()))
    os.remove(DOWNLOAD_STATUS)

if __name__ == '__main__':
    download_music()