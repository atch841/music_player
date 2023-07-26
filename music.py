import os
import subprocess
import time
import random
import json

from utils import log
from config import MUSIC_PATH, MSTATUS, MUSIC_META, FIFO_PATH

now = ''

try:
    os.mkfifo(FIFO_PATH)
except FileExistsError:
    print('fifo already exist')

while True:
    with open(MSTATUS, 'r') as file:
        cmd = file.readline().strip()
    print(cmd)
    if cmd == 'play':
        try:
            music_list = os.listdir(MUSIC_PATH)
            ind = random.randint(0, len(music_list) - 1)
            print('omxplayer-pi ' + MUSIC_PATH + os.listdir(MUSIC_PATH)[ind])
            
            music_meta = json.load(open(MUSIC_META, 'r'))
            vid = os.listdir(MUSIC_PATH)[ind].split('.')[0]
            if vid in music_meta.keys():
                log(f'now playing {music_meta[vid]}')

            now = MUSIC_PATH + music_list[ind]
            run_cmd = f'omxplayer-pi {os.path.join(MUSIC_PATH, music_list[ind])} < {FIFO_PATH}'
            os.system(run_cmd)
            os.system(f'echo -n z > {FIFO_PATH}')
        except Exception as e:
            print('error', e)
            log(f'error {e}')
            
    elif cmd == 'delete':
        if now:
            os.remove(now)
            print('remove', now)
            log(f'remove {now}')
        with open(MSTATUS, 'w') as file:
            file.write('play')
    time.sleep(1)
