from flask import Flask
from download_music import download_music, DOWNLOAD_STATUS
from threading import Thread
import os

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

@app.route("/delete")
def delete():
    with open('/home/ubuntu/mstatus', 'w') as file:
        file.write('delete')
    return 'delete'

@app.route('/download')
def download():
    if os.path.exists(DOWNLOAD_STATUS):
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
