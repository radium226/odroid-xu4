ARCHIVE_URL = http://os.archlinuxarm.org/os/ArchLinuxARM-odroid-xu3-latest.tar.gz
ARCHIVE_FILE_NAME = archlinux-arm.tar.gz
ROOTFS_FOLDER_NAME = rootfs

MODE = loop

./$(ROOTFS_FOLDER_NAME):
	mkdir -p "./$(ROOTFS_FOLDER_NAME)"

.PHONY: prepare-device
prepare-device:
	make -f "./Makefile.$(MODE)" prepare

.PHONY: mount-device
mount-device: ./$(ROOTFS_FOLDER_NAME)
	mountpoint -q -- "./$(ROOTFS_FOLDER_NAME)" || make -f "./Makefile.$(MODE)" mount ROOTFS_FOLDER_NAME="$(ROOTFS_FOLDER_NAME)"

./$(ARCHIVE_FILE_NAME):
	wget "$(ARCHIVE_URL)" -O "./$(ARCHIVE_FILE_NAME)"

.PHONY: extract-archive
extract-archive: ./mount-device ./$(ARCHIVE_FILE_NAME)
	sudo bsdtar -xpf "./$(ARCHIVE_FILE_NAME)" -C "./$(ROOTFS_FOLDER_NAME)"

.PHONY: setup-qemu
setup-qemu:
	sudo cp "/usr/bin/qemu-arm-static" "./$(ROOTFS_FOLDER_NAME)/usr/bin/qemu-arm-static"
	echo ':arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-arm-static:OC' | sudo tee "/proc/sys/fs/binfmt_misc/register" || true

.PHONY: chroot
chroot: mount-device
	sudo arch-chroot "./$(ROOTFS_FOLDER_NAME)" /bin/bash

.PHONY: bootstrap-rootfs
bootstrap-rootfs: setup-qemu
	sudo cp "./bootstrap.sh" "./$(ROOTFS_FOLDER_NAME)/usr/local/bin/bootstrap.sh"
	sudo arch-chroot "./$(ROOTFS_FOLDER_NAME)" "/usr/local/bin/bootstrap.sh"

.PHONY:
unmount-device:
	mountpoint -q -- "./$(ROOTFS_FOLDER_NAME)" && sudo umount "./$(ROOTFS_FOLDER_NAME)"

.PHONY: fuse-device
fuse-device:
	make -f "./Makefile.$(MODE)" fuse ROOTFS_FOLDER_NAME="$(ROOTFS_FOLDER_NAME)"

.PHONY: build
build: prepare-device mount-device extract-archive bootstrap-rootfs fuse-device unmount-device

.PHONY: start-dns
start-dns:
	make -f "./Makefile.dns" start

.PHONY: stop-dns
stop-dns:
	make -f "./Makefile.dns" stop

.PHONY: clean
clean:
	sudo pkill -9 "bootstrap.sh" || true
	@sleep 1
	mountpoint -q -- "./$(ROOTFS_FOLDER_NAME)" && sudo umount "./$(ROOTFS_FOLDER_NAME)" || true
	make -f "./Makefile.$(MODE)" clean
	#test -f "./$(ARCHIVE_FILE_NAME)" && rm -Rf "./$(ARCHIVE_FILE_NAME)" || true
	test -d "./$(ROOTFS_FOLDER_NAME)" && rm -Rf "./$(ROOTFS_FOLDER_NAME)" || true
