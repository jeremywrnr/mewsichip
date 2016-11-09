#!/bin/bash 

# setup script for mewsician chip (mewsichip)

# setting up CHIP python
sudo apt-get update
sudo apt-get install git build-essential python-dev python-pip flex bison -y
git clone https://github.com/atenart/dtc
cd dtc
make
sudo  make install PREFIX=/usr
cd ..
git clone git://github.com/xtacocorex/CHIP_IO.git
cd CHIP_IO
sudo python setup.py install
cd ..
sudo rm -rf CHIP_IO

# enable setup and connect commands
# ./setup - prep wifi connection
# ./connect <ssid> <pass>
git clone https://github.com/jeremywrnr/mewsichip
source networking.sh
