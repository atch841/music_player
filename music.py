import os
import subprocess
import time
import random


MUSIC_PATH = '/home/ubuntu/music/'
MSTATUS = '/home/ubuntu/mstatus'
now = ''

while True:
    with open(MSTATUS, 'r') as file:
        cmd = file.readline().strip()
    if cmd == 'play':
        try:
            ind = random.randint(0, len(os.listdir(MUSIC_PATH) - 1))
            print('omxplayer-pi ' + MUSIC_PATH + os.listdir(MUSIC_PATH)[ind])
            now = MUSIC_PATH + os.listdir(MUSIC_PATH)[ind]
            os.system('omxplayer-pi ' + MUSIC_PATH + os.listdir(MUSIC_PATH)[ind])
        except:
            print('error')
    elif cmd == 'delete':
        if now:
            os.remove(now)
        with open(MSTATUS, 'w') as file:
            file.write('play')
    time.sleep(1)
