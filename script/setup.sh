#!/bin/bash

# setup script for mewsician chip (mewsichip)

# setting up CHIP python gpio library
cd "$HOME" && sudo apt-get update
sudo apt-get install git build-essential python-dev python-pip flex bison -y
git clone https://github.com/atenart/dtc
cd dtc && make && sudo make install PREFIX=/usr
cd .. && git clone git://github.com/xtacocorex/CHIP_IO.git
cd CHIP_IO && sudo python setup.py install
cd .. && sudo rm -rf CHIP_IO
sudo pip install psutil

# clone mplayer defaut configuration and set it up
wget -O input.conf https://raw.githubusercontent.com/williambelle/mplayer-config/master/input.conf
mkdir -p "$HOME/.mplayer/" && mv input.conf "$HOME/.mplayer/"

# hacky time update from the scourges of the internt
# https://askubuntu.com/questions/81293/what-is-the-command-to-update-time-and-date-from-internet
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

# TODO optimize this for the latest targeted firmware
git clone https://github.com/jeremywrnr/mewsichip

# share wifi connection chip details
echo "for wifi run: mewsichip/connect.sh <ssid> <pass>"
