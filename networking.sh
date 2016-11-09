# source these functions when getting started on the chip
# install the ssh agent

ip-setup() {
  sudo apt-get install avahi-daemon
}

# disable any networks, and connect to specified arguments
# $1 - network name
# $2 - network pass

connect() {
  sudo nmcli dev disconnect wlan0
  sudo nmcli device wifi connect "$1" password "$2" ifname wlan0
}
