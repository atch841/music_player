import os
import random
import json
import time

from utils import log
from omxplayer.player import OMXPlayer
from config import MUSIC_PATH, MSTATUS, MUSIC_META, FIFO_PATH, NOW_PLAYING, VOL_ALL
from config import OMX_CMD
from download_music import MUSIC_META_NAME, MUSIC_META_VOL

player = None

class Player:
    def __init__(self):
        self.vol = 100
        self.vol_all = 100

    def select_song(self):
        music_list = os.listdir(MUSIC_PATH)
        ind = random.randint(0, len(music_list) - 1)
        
        music_meta = json.load(open(MUSIC_META, 'r'))
        vid = os.listdir(MUSIC_PATH)[ind].split('.')[0]
        if vid in music_meta.keys():
            log(f'now playing {music_meta[vid][MUSIC_META_NAME]}')
            self.vol = music_meta[vid][MUSIC_META_VOL]
        else:
            self.vol = 100

        music_path = os.path.join(MUSIC_PATH, music_list[ind])
        with open(NOW_PLAYING, 'w') as file:
            file.write(music_path)

        if os.path.exists(VOL_ALL):
            with open(VOL_ALL, 'r') as file:
                self.vol_all = int(file.readline().strip())
        else:
            self.vol_all = 100

        return music_path

    def play(self):
        music_path = self.select_song()

        def next_song(_, exit_code):
            print('exit:', exit_code)
            if exit_code != 3:
                global player
                music_path = self.select_song()
                player = OMXPlayer(music_path)
                player.exitEvent += next_song

                # adjust volume
                time.sleep(2.5)  # wait for the music to start
                set_vol = (self.vol + self.vol_all - 100) / 100
                print('vol:', set_vol)
                player.set_volume(set_vol)

        global player
        player = OMXPlayer(music_path)
        player.exitEvent += next_song

        # adjust volume
        time.sleep(2.5)  # wait for the music to start
        set_vol = (self.vol + self.vol_all - 100) / 100
        print('vol:', set_vol)
        player.set_volume(set_vol)
        
    def stop(self):
        global player
        player.stop()

    def vol_up(self):
        global player
        player.set_volume(player.volume() + 0.1)

    def vol_down(self):
        global player
        player.set_volume(player.volume() - 0.1)