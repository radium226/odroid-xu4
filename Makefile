ARCHIVE_URL = http://os.archlinuxarm.org/os/ArchLinuxARM-odroid-xu3-latest.tar.gz
ARCHIVE_FILE_NAME = archlinux-arm.tar.gz
ROOTFS_FOLDER_NAME = rootfs

DEVICE = loop

./$(ROOTFS_FOLDER_NAME):
	mkdir -p "./$(ROOTFS_FOLDER_NAME)"

.PHONY: device-prepare
device-prepare:
	make -f "./Makefile.$(DEVICE)" prepare

.PHONY: device-mount
device-mount: ./$(ROOTFS_FOLDER_NAME)
	mountpoint -q -- "./$(ROOTFS_FOLDER_NAME)" || make -f "./Makefile.$(DEVICE)" mount ROOTFS_FOLDER_NAME="$(ROOTFS_FOLDER_NAME)"

./$(ARCHIVE_FILE_NAME):
	wget "$(ARCHIVE_URL)" -O "./$(ARCHIVE_FILE_NAME)"

.PHONY: archive-extract
archive-extract: ./device-mount ./$(ARCHIVE_FILE_NAME)
	sudo bsdtar -xpf "./$(ARCHIVE_FILE_NAME)" -C "./$(ROOTFS_FOLDER_NAME)"

.PHONY: rootfs-copy-qemu
rootfs-copy-qemu:
	sudo cp "/usr/bin/qemu-arm-static" "./$(ROOTFS_FOLDER_NAME)/usr/bin/qemu-arm-static"
	echo ':arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-arm-static:OC' | sudo tee "/proc/sys/fs/binfmt_misc/register" || true

.PHONY: chroot
chroot: device-mount
	sudo arch-chroot "./$(ROOTFS_FOLDER_NAME)" /bin/bash

.PHONY: rootfs-copy-bootstrap
rootfs-copy-bootstrap:
	sudo rm -Rf "./$(ROOTFS_FOLDER_NAME)/var/local/lib/bootstrap" || true
	tar -C "./bootstrap" -cf - "." | sudo tar xf - --overwrite -C "./$(ROOTFS_FOLDER_NAME)"

.PHONY: rootfs-bootstrap
rootfs-bootstrap: rootfs-copy-qemu rootfs-copy-bootstrap
	sudo arch-chroot "./$(ROOTFS_FOLDER_NAME)" "/usr/local/bin/bootstrap"

.PHONY: rootfs-ansible-playbook
rootfs-ansible-playbook: rootfs-copy-qemu rootfs-copy-bootstrap
	sudo arch-chroot "./$(ROOTFS_FOLDER_NAME)" "/usr/local/bin/bootstrap" "ansible-playbook"

.PHONY:
device-unmount:
	mountpoint -q -- "./$(ROOTFS_FOLDER_NAME)" && sudo umount "./$(ROOTFS_FOLDER_NAME)"

.PHONY: device-fuse
device-fuse:
	make -f "./Makefile.$(DEVICE)" fuse ROOTFS_FOLDER_NAME="$(ROOTFS_FOLDER_NAME)"

.PHONY: build
build: device-prepare device-mount archive-extract rootfs-bootstrap device-fuse device-unmount

.PHONY: dns-start
dns-start:
	make -f "./Makefile.dns" start

.PHONY: dns-stop
dns-stop:
	make -f "./Makefile.dns" stop

.PHONY: cloud-init
cloud-init: rootfs-bootstrap
	sudo arch-chroot "./$(ROOTFS_FOLDER_NAME)" sh -c '/usr/bin/cloud-init clean && cloud-init --debug modules --mode config'

.PHONY: clean
clean:
	sudo pkill -9 "bootstrap" || true
	@sleep 1
	mountpoint -q -- "./$(ROOTFS_FOLDER_NAME)" && sudo umount "./$(ROOTFS_FOLDER_NAME)" || true
	make -f "./Makefile.$(DEVICE)" clean
	#test -f "./$(ARCHIVE_FILE_NAME)" && rm -Rf "./$(ARCHIVE_FILE_NAME)" || true
	test -d "./$(ROOTFS_FOLDER_NAME)" && rm -Rf "./$(ROOTFS_FOLDER_NAME)" || true
	make -f "./Makefile.dns" clean

PORT = 80
.PHONY: tools-nmap
tools-nmap:
	make -f "./Makefile.tools" nmap PORT="$(PORT)"

COMMAND = bash -il
.PHONY: tools-ssh
tools-ssh:
	make -f "./Makefile.tools" ssh COMMAND="$(COMMAND)"
