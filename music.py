import os
import subprocess
import time
import random


path = '/home/ubuntu/music/'

while True:
    with open('/home/ubuntu/mstatus', 'r') as file:
        cmd = file.readline().strip()
    if cmd == 'play':
        try:
            ind = random.randint(0, len(os.listdir(path) - 1))
            print('omxplayer-pi ' + path + os.listdir(path)[ind])
            os.system('omxplayer-pi ' + path + os.listdir(path)[ind])
        except:
            print('error')
    time.sleep(1)
