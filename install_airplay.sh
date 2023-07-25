# ref: https://linuxhint.com/turn-raspberry-pi-into-airplay-receiver/
cd ~
sudo apt update
sudo apt install autoconf libconfig-dev libtool libasound2-dev libpopt-dev libdaemon-dev avahi-daemon libavahi-client-dev libssl-dev -y
git clone https://github.com/mikebrady/shairport-sync.git
cd shairport-sync
autoreconf -i -f
./configure --with-alsa --with-avahi --with-ssl=openssl --with-systemd --with-metadata
make
sudo make install
sudo systemctl enable shairport-sync
sudo systemctl start shairport-sync
sudo systemctl status shairport-sync