# ODROID XU4

## Requirements
* `sudo`
* `make`
* `dnsmasq`
* `gcc` (for applying macro)
* `wget`
* `curl`
* `arch-install-scripts` (for `arch-chroot`)
* `bsdtar` (for extracting the official Arch Linux ARM image)

## Usage
* Start the DNS server to allow direct Ethernet connection with the board: `make start-dns`
* Stop the DNS Server: `make stop-dns`
* Build an Arch Linux install into a loopback device: `make build MODE="loop"`
* Build an Arch Linux install into the `/dev/sdb` SD-Card: `make build MODE="sd"` 
