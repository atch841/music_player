import requests
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
import os


def get_music(vid):
    url = f"https://www.youtube.com/watch?v={vid}"
    yt = YouTube(url)
    print(vid + ".mp3")
    _filename = '/home/ubuntu/music/' + vid + ".mp3"
    if vid + ".mp3" not in os.listdir('/home/ubuntu/music/'):
        yt.streams.get_audio_only().download(filename=_filename)

DEVELOPER_KEY = ''
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)



r = requests.get('https://kma.kkbox.com/charts/api/v1/yearly?category=297&lang=tc&limit=100&terr=tw&type=newrelease&year=2022')

song_name = []
for song in json.loads(r.text)['data']['charts']['newrelease']:
    song_name.append(song['song_name'])


for song in song_name:

    request = youtube.search().list(part="snippet",q=song)
    response = request.execute()

    get_music(response['items'][0]['id']['videoId'])
