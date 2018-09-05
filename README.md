# ODROID XU4

## Usage
* Start the DNS server to allow direct Ethernet connection with the board: `make start-dns`
* Stop the DNS Server: `make stop-dns`
* Build an Arch Linux install into a loopback device: `make build MODE="loop"`
* Build an Arch Linux install into the `/dev/sdb` SD-Card: `make build MODE="sd"` 
