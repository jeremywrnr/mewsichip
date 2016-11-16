# disable current network connection, and connect to specified arguments
# $1 - network name
# $2 - network pass

connect() {
    sudo nmcli dev disconnect wlan0
    sudo nmcli device wifi connect "$1" password "$2" ifname wlan0
}
