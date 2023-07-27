import os
APP_FOLDER = '/home/ubuntu/music_player_data/'
DOWNLOAD_STATUS = os.path.join(APP_FOLDER, 'download_status')
MUSIC_META = os.path.join(APP_FOLDER, 'music_meta')
VID_LOOKUP = os.path.join(APP_FOLDER, 'vid_lookup')
MUSIC_PATH = os.path.join(APP_FOLDER, 'music/')
MSTATUS = os.path.join(APP_FOLDER, 'mstatus')
LOG = os.path.join(APP_FOLDER, 'log')
DEV_KEY = os.path.join(APP_FOLDER, '.dev_key')
FIFO_PATH = os.path.join(APP_FOLDER, 'fifo')
NOW_PLAYING = os.path.join(APP_FOLDER, 'now_playing')
VOL_ALL = os.path.join(APP_FOLDER, 'vol_all')
OMX_CMD = 'omxplayer-pi'
SONG_URL = 'https://www.youtube.com/playlist?list=PL5qh1a9hXNSd9ReRdKyuYysCdGVhCmouz'

os.makedirs(APP_FOLDER, exist_ok=True)
if not os.path.exists(MSTATUS):
    with open(MSTATUS, 'w') as file:
        file.write('stop')