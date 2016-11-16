[mewsichip](http://mewsician.win) :cat2:
========================================

Embedded code for the CHIP for the mewsician project.


### new chip

    curl https://raw.githubusercontent.com/jeremywrnr/mewsichip/master/script/mewsetup.sh | bash

### resources

- [chip gpio documentation](http://docs.getchip.com/chip.html#physical-connectors)
- [headphone jack diagram](http://www.cablechick.com.au/resources/image/trrs-diagram2.jpg)
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

