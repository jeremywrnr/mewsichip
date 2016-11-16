# disable current network connection, and connect to specified arguments
# $1 - network name (ssid)
# $2 - network password

sudo nmcli dev disconnect wlan0
sudo nmcli device wifi connect "$1" password "$2" ifname wlan0
