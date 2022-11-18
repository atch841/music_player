import time
from flask import Flask
import random
from threading import Thread
import os
import subprocess

def play_music():
    path = '/home/ubuntu/music/'

    while True:
        with open('/home/ubuntu/mstatus', 'r') as file:
            cmd = file.readline().strip()
        if cmd == 'play':
                ind = random.randint(0, len(os.listdir(path)))
                print('omxplayer-pi ' + path + os.listdir(path)[ind])
                p = subprocess.Popen(['omxplayer-pi', path + os.listdir(path)[ind]])
                p.wait()
        time.sleep(1)




app = Flask(__name__)


@app.route("/play")
def play():
    with open('/home/ubuntu/mstatus', 'w') as file:
        file.write('play')

    return 'play'

@app.route("/stop")
def stop():
    with open('/home/ubuntu/mstatus', 'w') as file:
        file.write('stop')
    return 'stop'


if __name__ == '__main__':
    music_thread = Thread(target=play_music)
    music_thread.start()
    app.run(debug=True, host='0.0.0.0', port=80)
