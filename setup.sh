#!/bin/bash 

# setup script for mewsician chip (mewsichip)

cd "$HOME"
sudo apt-get update
sudo apt-get install git
git clone https://github.com/jeremywrnr/mewsichip
source networking.sh
