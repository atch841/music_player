import requests
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
import os

DOWNLOAD_STATUS = '/home/ubuntu/download_status'
MUSIC_META = '/home/ubuntu/music_meta'

def get_music(vid):
    url = f"https://www.youtube.com/watch?v={vid}"
    yt = YouTube(url)
    print(vid + ".mp3")
    _filename = '/home/ubuntu/music/' + vid + ".mp3"
    if vid + ".mp3" not in os.listdir('/home/ubuntu/music/'):
        yt.streams.get_audio_only().download(filename=_filename)

def download_music():
    with open('/home/ubuntu/.dev_key',  'r') as file:
        developerKey = file.read().strip()
    youtube = build('youtube', 'v3', developerKey=developerKey)

    if os.path.exists(MUSIC_META):
        music_meta = json.load(open(MUSIC_META, 'r'))
    else:
        music_meta = {}

    r = requests.get('https://kma.kkbox.com/charts/api/v1/yearly?category=297&lang=tc&limit=100&terr=tw&type=newrelease&year=2022')

    song_name = []
    for song in json.loads(r.text)['data']['charts']['newrelease']:
        song_name.append(song['song_name'])

    print('songs:', song_name)

    for idx, song in enumerate(song_name):
        with open(DOWNLOAD_STATUS, 'w') as file:
            file.write(f'{idx}/{len(song_name)}')

        request = youtube.search().list(part="snippet",q=song)
        response = request.execute()

        vid = response['items'][0]['id']['videoId']
        get_music(vid)
        music_meta[vid] = {'name': song, 'volume': 100}
        json.dump(music_meta, open(MUSIC_META, 'w'))


if __name__ == '__maiu__':
    download_music()