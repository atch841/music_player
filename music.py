import os
import time
import random
import json

from utils import log
from config import MUSIC_PATH, MSTATUS, MUSIC_META, FIFO_PATH, NOW_PLAYING, VOL_ALL
from download_music import MUSIC_META_NAME, MUSIC_META_VOL

now = ''

try:
    os.mkfifo(FIFO_PATH)
except FileExistsError:
    print('fifo already exist')

while True:
    with open(MSTATUS, 'r') as file:
        cmd = file.readline().strip()

    with open(NOW_PLAYING, 'r') as file:
        now = file.readline().strip()
    print(cmd, now)

    if cmd == 'play' and now == '':
        try:
            music_list = os.listdir(MUSIC_PATH)
            ind = random.randint(0, len(music_list) - 1)
            print('omxplayer-pi ' + MUSIC_PATH + os.listdir(MUSIC_PATH)[ind])
            
            music_meta = json.load(open(MUSIC_META, 'r'))
            vid = os.listdir(MUSIC_PATH)[ind].split('.')[0]
            if vid in music_meta.keys():
                log(f'now playing {music_meta[vid][MUSIC_META_NAME]}')
                vol = music_meta[vid][MUSIC_META_VOL]
            else:
                vol = 100

            music_path = os.path.join(MUSIC_PATH, music_list[ind])
            with open(NOW_PLAYING, 'w') as file:
                file.write(music_path)

            run_cmd = f'omxplayer-pi {music_path} < {FIFO_PATH} && echo "" > {NOW_PLAYING} || echo "" > {NOW_PLAYING} &'
            os.system(run_cmd)
            os.system(f'echo -n z > {FIFO_PATH}')

            # adjust volume
            while vol != 100:
                if vol > 100:
                    vol -= 10
                    os.system(f'echo -n + > {FIFO_PATH}')
                elif vol < 100:
                    vol += 10
                    os.system(f'echo -n - > {FIFO_PATH}')
                    
            with open(VOL_ALL, 'r') as file:
                vol_all = int(file.readline().strip())
            while vol_all != 100:
                if vol_all > 100:
                    vol_all -= 10
                    os.system(f'echo -n + > {FIFO_PATH}')
                elif vol_all < 100:
                    vol_all += 10
                    os.system(f'echo -n - > {FIFO_PATH}')

        except Exception as e:
            print('error', e)
            log(f'error {e}')

    # elif cmd == 'delete':
    #     if now:
    #         os.remove(now)
    #         print('remove', now)
    #         log(f'remove {now}')
    #     with open(MSTATUS, 'w') as file:
    #         file.write('play')
    time.sleep(1)
