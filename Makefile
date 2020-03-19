WORK_FOLDER_PATH = work

ARCHIVE_URL = http://os.archlinuxarm.org/os/ArchLinuxARM-odroid-xu3-latest.tar.gz
ARCHIVE_FILE_NAME = archlinux-arm.tar.gz

ROOTFS_FOLDER_NAME = rootfs

IMAGE_FILE_NAME = sd-card.img
IMAGE_FILE_SIZE = 4G
IMAGE_PARTITION_LABEL = ROOT

CONTAINER_NAME = odroid-xu4

$(WORK_FOLDER_PATH)/$(IMAGE_FILE_NAME):
	mkdir -p "$(WORK_FOLDER_PATH)"
	dd of="$(WORK_FOLDER_PATH)/$(IMAGE_FILE_NAME)" bs=1 seek="$(IMAGE_FILE_SIZE)" count=0
	mkfs.ext4 -F "$(WORK_FOLDER_PATH)/$(IMAGE_FILE_NAME)" -L "$(IMAGE_PARTITION_LABEL)"

.PHONY: clean
clean:
	sudo rm -Rf "$(WORK_FOLDER_PATH)" || true

.PHONY: mount
mount: $(WORK_FOLDER_PATH)/$(IMAGE_FILE_NAME)
	mkdir -p "$(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)"
	sudo mount -o "suid" "$(WORK_FOLDER_PATH)/$(IMAGE_FILE_NAME)" "$(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)"

# Download latest Arch Linux image
$(WORK_FOLDER_PATH)/$(ARCHIVE_FILE_NAME):
	wget "$(ARCHIVE_URL)" -O "$(WORK_FOLDER_PATH)/$(ARCHIVE_FILE_NAME)"

# Copy qemu and register for binfmt
$(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)/usr/bin/qemu-arm-static:
	sudo cp "/usr/bin/qemu-arm-static" "$(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)/usr/bin/qemu-arm-static"
	echo ':arm:M::\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x28\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-arm-static:OC' | sudo tee "/proc/sys/fs/binfmt_misc/register" || true

.PHONY: archive-extract
archive-extract: mount $(WORK_FOLDER_PATH)/$(ARCHIVE_FILE_NAME)
		sudo bsdtar -xpf "$(WORK_FOLDER_PATH)/$(ARCHIVE_FILE_NAME)" -C "$(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)"

.PHONY: build
build: mount archive-extract

.PHONY: shell
shell: $(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)/usr/bin/qemu-arm-static
	sudo systemd-nspawn \
		--boot \
		--machine="$(CONTAINER_NAME)" \
		--directory="$(WORK_FOLDER_PATH)/$(ROOTFS_FOLDER_NAME)"
		--bind-ro="/etc/resolv.conf:/run/systemd/resolve/resolv.conf"
