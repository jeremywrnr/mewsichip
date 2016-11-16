mewsichip :cat2:
================

Embedded code for the CHIP for the mewsician project.


### resources

- [chip gpio diagram](http://docs.getchip.com/images/chip_pinouts.jpg)
- [headphone jack](http://www.cablechick.com.au/resources/image/trrs-diagram2.jpg)
- [mewsician repo](https://github.com/radiolarian/mewsician)


### commands

list wifi spots

    nmcli device wifi list

connect to wifi

    sudo nmcli device wifi connect "$1" password "$2" ifname wlan0

turn off wifi

    sudo nmcli dev disconnect wlan0

check the internet

    ping 8.8.8.8

setup ssh agent

    sudo apt-get install avahi-daemon

