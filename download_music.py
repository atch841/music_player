import json
import re
import os
import traceback
import urllib.request
import urllib
from pytube import YouTube
from pytube.cli import on_progress
from pytube import Playlist

from config import DOWNLOAD_STATUS, MUSIC_META, MUSIC_PATH
from config import SONG_URL
from utils import log

MUSIC_META_NAME = 'name'
MUSIC_META_VOL = 'volume'


def get_music(vid):
    url = f"https://www.youtube.com/watch?v={vid}"
    yt = YouTube(url, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)
    print(vid + ".mp3")
    _filename = MUSIC_PATH + vid + ".mp3"
    if vid + ".mp3" not in os.listdir(MUSIC_PATH):
        yt.streams.get_audio_only().download(filename=_filename)

def get_vid(song_url):
    # get vid from song url
    vid = song_url[song_url.find('=')+1:]
    return vid

def get_song_name(VideoID):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data['title']

def get_song(song_url):
    if os.path.exists(MUSIC_META):
        music_meta = json.load(open(MUSIC_META, 'r'))
    else:
        music_meta = {}

    vid = get_vid(song_url)

    if vid in music_meta.keys():
        return
    get_music(vid)
    music_meta[vid] = {MUSIC_META_NAME: get_song_name(vid), MUSIC_META_VOL: 100}
    json.dump(music_meta, open(MUSIC_META, 'w'))
    

def download_music():
    os.makedirs(os.path.dirname(DOWNLOAD_STATUS), exist_ok=True)
    os.makedirs(MUSIC_PATH, exist_ok=True)

    playlist = Playlist(SONG_URL)

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    urls = playlist.video_urls

    for idx, song in enumerate(urls):
        with open(DOWNLOAD_STATUS, 'w') as file:
            file.write(f'{idx}/{len(urls)}')
        log(f'downloading {song} ({idx}/{len(urls)})')

        try:
            get_song(song)
        except Exception:
            print(traceback.format_exc())
            log(str(traceback.format_exc()))
    os.remove(DOWNLOAD_STATUS)

if __name__ == '__main__':
    download_music()