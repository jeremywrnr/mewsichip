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

# TODO optimize this for the latest targeted firmware
git clone https://github.com/jeremywrnr/mewsichip

# share wifi connection chip details
echo "for wifi run: mewsichip/connect.sh <ssid> <pass>"
