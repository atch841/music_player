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


def get_song(song_name):
    if os.path.exists(MUSIC_META):
        music_meta = json.load(open(MUSIC_META, 'r'))
    else:
        music_meta = {}

    with open('/home/ubuntu/.dev_key',  'r') as file:
        developerKey = file.read().strip()
    youtube = build('youtube', 'v3', developerKey=developerKey)

    request = youtube.search().list(part="snippet",q=song_name)
    response = request.execute()

    vid = response['items'][0]['id']['videoId']
    if vid in music_meta.keys():
        return
    get_music(vid)
    music_meta[vid] = {'name': song_name, 'volume': 100}
    json.dump(music_meta, open(MUSIC_META, 'w'))
    

def download_music():

    r = requests.get('https://kma.kkbox.com/charts/api/v1/yearly?category=297&lang=tc&limit=100&terr=tw&type=newrelease&year=2022')

    song_name = []
    for song in json.loads(r.text)['data']['charts']['newrelease']:
        song_name.append(song['song_name'])

    print('songs:', song_name)

    for idx, song in enumerate(song_name):
        with open(DOWNLOAD_STATUS, 'w') as file:
            file.write(f'{idx}/{len(song_name)}')

        get_song(song)
    os.remove(DOWNLOAD_STATUS)

if __name__ == '__main__':
    download_music()