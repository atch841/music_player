import os
APP_FOLDER = '/home/ubuntu/music_player_data/'
DOWNLOAD_STATUS = os.path.join(APP_FOLDER, 'download_status')
MUSIC_META = os.path.join(APP_FOLDER, 'music_meta')
VID_LOOKUP = os.path.join(APP_FOLDER, 'vid_lookup')
MUSIC_PATH = os.path.join(APP_FOLDER, 'music/')
MSTATUS = os.path.join(APP_FOLDER, 'mstatus')
LOG = os.path.join(APP_FOLDER, 'log')
DEV_KEY = os.path.join(APP_FOLDER, '.dev_key')
FIFO_PATH = os.path.join(APP_FOLDER, 'fifo/')
SONG_URL = 'https://kma.kkbox.com/charts/api/v1/yearly?category=297&lang=tc&limit=100&terr=tw&type=newrelease&year=2023'