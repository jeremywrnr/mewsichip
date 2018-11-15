[mewsichip](http://mewsician.win) :cat2:
========================================

[![final project video](http://img.youtube.com/vi/hWpbkYcAkbg/0.jpg)](http://www.youtube.com/watch?v=hWpbkYcAkbg)

Embedded code for the CHIP for the mewsician project.


### setup new chip

    curl https://raw.githubusercontent.com/jeremywrnr/mewsichip/master/script/mewsetup.sh | bash


### resources

- [mewsician website](https://github.com/jeremywrnr/mewsichip)
- [mewsician github repo](https://github.com/radiolarian/mewsician)
- [chip gpio documentation](http://docs.getchip.com/chip.html#physical-connectors)
- [adafruit headphone schematic](https://cdn-shop.adafruit.com/product-files/1699/STX3120.pdf)
- [systemd CHIP setup help](https://github.com/fordsfords/blink)
- [headphone jack diagram](http://www.cablechick.com.au/resources/image/trrs-diagram2.jpg)


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

restart mew service

    sudo systemctl restart mew


### demo videos

alpha workflow

[![alpha prototype demo video](http://img.youtube.com/vi/-4KjWFd3zv4/0.jpg)](http://www.youtube.com/watch?v=-4KjWFd3zv4)

hardware / server link

[![hardware prototype demo video](http://img.youtube.com/vi/5e9CuM0uRTQ/0.jpg)](http://www.youtube.com/watch?v=5e9CuM0uRTQ)

