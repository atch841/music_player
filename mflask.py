from flask import Flask
from threading import Thread
import subprocess
import os
import time
import json

from utils import read_log
from download_music import download_music, DOWNLOAD_STATUS, MUSIC_META_VOL, MUSIC_META_NAME
from config import MSTATUS, MUSIC_META, FIFO_PATH, NOW_PLAYING, VOL_ALL
from player import Player

# p = subprocess.Popen(['/bin/sh', 'run_music.sh'])

p = Player()

app = Flask(__name__)


@app.route("/log")
def log():
    return read_log()

@app.route("/play")
def play():
    # with open(MSTATUS, 'w') as file:
    #     file.write('play')
    p.play()

    return 'play'

@app.route("/stop")
def stop():
    # with open(MSTATUS, 'w') as file:
    #     file.write('stop')
    # os.system(f'echo -n q > {FIFO_PATH}')
    p.stop()
    return 'stop'

@app.route("/delete")
def delete():
    # with open(MSTATUS, 'w') as file:
    #     file.write('delete')
    with open(NOW_PLAYING, 'r') as file:
        now = file.readline().strip()
    # os.system(f'echo -n q > {FIFO_PATH}')
    p.stop()
    if now:
        os.remove(now)
        print('remove', now)
        log(f'remove {now}')
    return 'delete'


@app.route('/download')
def download():
    if os.path.exists(DOWNLOAD_STATUS) and time.time() - os.path.getmtime(DOWNLOAD_STATUS) < 60*60:
        return 'already downloading'
    else:
        download_thread = Thread(target=download_music)
        download_thread.start()
        return 'start!'

@app.route('/download_status')
def download_status():
    if os.path.exists(DOWNLOAD_STATUS):
        with open(DOWNLOAD_STATUS, 'r') as file:
            status = file.read()
        return status
    else:
        return 'Not downloading'

@app.route('/vol_up_all')
def vol_up_all():
    if os.path.exists(VOL_ALL):
        with open(VOL_ALL, 'r') as file:
            vol = float(file.readline().strip())
    else:
        vol = 100
    vol *= 2
    with open(VOL_ALL, 'w') as file:
        file.write(str(vol))
    # os.system(f'echo -n + > {FIFO_PATH}')
    p.vol_up()
    return f"all volume up {vol}"


@app.route('/vol_down_all')
def vol_down_all():
    if os.path.exists(VOL_ALL):
        with open(VOL_ALL, 'r') as file:
            vol = float(file.readline().strip())
    else:
        vol = 100
    vol /= 2
    with open(VOL_ALL, 'w') as file:
        file.write(str(vol))
    # os.system(f'echo -n - > {FIFO_PATH}')
    p.vol_down()
    return f"all volume down {vol}"

@app.route('/vol_up')
def vol_up():
    with open(NOW_PLAYING, 'r') as file:
        now = file.readline().strip()
    if now == "":
        return "no music playing"
    music_meta = json.load(open(MUSIC_META, 'r'))
    # /path/to/music/vid.mp3 to vid
    vid = now.split('/')[-1].split('.')[0]
    if vid in music_meta:
        vol = music_meta[vid][MUSIC_META_VOL]
    else:
        vol = 100
        music_meta[vid] = {MUSIC_META_NAME: 'unknow', MUSIC_META_VOL: vol}
    vol *= 2
    music_meta[vid][MUSIC_META_VOL] = vol
    json.dump(music_meta, open(MUSIC_META, 'w'))
    # os.system(f'echo -n + > {FIFO_PATH}')
    p.vol_up()
    return f'music vol up {vol}'

@app.route('/vol_down')
def vol_down():
    with open(NOW_PLAYING, 'r') as file:
        now = file.readline().strip()
    if now == "":
        return "no music playing"
    music_meta = json.load(open(MUSIC_META, 'r'))
    # /path/to/music/vid.mp3 to vid
    vid = now.split('/')[-1].split('.')[0]
    if vid in music_meta:
        vol = music_meta[vid][MUSIC_META_VOL]
    else:
        vol = 100
        music_meta[vid] = {MUSIC_META_NAME: 'unknow', MUSIC_META_VOL: vol}
    vol /= 2
    music_meta[vid][MUSIC_META_VOL] = vol
    json.dump(music_meta, open(MUSIC_META, 'w'))
    # os.system(f'echo -n - > {FIFO_PATH}')
    p.vol_down()
    return f'music vol down {vol}'

@app.route('/update')
def update():
    os.system('git pull')
    # os.kill(p)
    # p = subprocess.Popen(['/bin/sh', 'run_music.sh'])

@app.route('/now')
def now():
    with open(NOW_PLAYING, 'r') as file:
        now = file.readline().strip()
    if now == "":
        return "no music playing"
    music_meta = json.load(open(MUSIC_META, 'r'))
    # /path/to/music/vid.mp3 to vid
    vid = now.split('/')[-1].split('.')[0]
    if vid in music_meta:
        name = music_meta[vid][MUSIC_META_NAME]
    return name


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
