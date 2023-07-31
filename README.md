# Raspberry Pi Music Player

## Branches
- master: using kkbox playlist (youtube api required)
- ytplaylist: using youtube playlist

## Setup
1. install Raspberry Pi OS Buster on raspberry pi (https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-legacy)
2. install petchelf: https://snapcraft.io/install/patchelf/raspbian
3. clone this repo
4. install requirements (`sudo pip3 install -r requirement.txt`)
5. modify config.py

## Usage
`sudo python3 mflast.py`

## APIs
### play and stop
- /play
- /stop
### adjust volume for the song
- /vol_up
- /vol_down
### adjust overall volume
- /vol_up_all
- /vol_down_all
### download/update musics
- /download
### status
- /now
- /log
- /download_status