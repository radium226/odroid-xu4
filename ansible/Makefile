CONTAINER_NAME = odroid-xu4

PLAYBOOK_FILE_NAME = provision.yml

./.$(CONTAINER_NAME):
	mkdir -p "./.$(CONTAINER_NAME)"

.PHONY: pacstrap
pacstrap: ./.$(CONTAINER_NAME)
	if ! find "./.$(CONTAINER_NAME)" -mindepth 1 2>"/dev/null"| read; then \
		sudo pacstrap \
			-c \
			"./.$(CONTAINER_NAME)" \
			"base" "python" ; \
	fi

.PHONY: systemd-nspawn
systemd-nspawn: pacstrap
	if ! sudo machinectl status "$(CONTAINER_NAME)" >"/dev/null"; then \
		sudo nohup systemd-nspawn \
			--boot \
			--machine="$(CONTAINER_NAME)" \
			--directory="./.$(CONTAINER_NAME)" >"./.$(CONTAINER_NAME).log" & \
	fi

./library:
	mkdir -p "./library"

./library/yay: ./library
	wget "https://raw.githubusercontent.com/mnussbaum/ansible-yay/master/yay" \
		-O "./library/yay"

.PHONY: ansible-playbook
ansible-playbook: systemd-nspawn ./library/yay
	sudo ansible-playbook \
		--inventory="./inventory.ini" \
		--connection="systemd-nspawn" \
		"./$(PLAYBOOK_FILE_NAME)"

.PHONY: clean
clean:
	machinectl poweroff "$(CONTAINER_NAME)"
	rm -Rf "./.$(CONTAINER_NAME)"

.PHONY: machinectl-stop
machinectl-stop:
	sudo machinectl poweroff "$(CONTAINER_NAME)"

.PHONY: machinectl-shell
machinectl-shell:
	sudo machinectl shell "$(CONTAINER_NAME)"


# Provisionning

TARGET = remote
HOST_NAME = odroid-xu4.local

.PHONY: provision
provision: provision-$(TARGET)

.PHONY: provision-remote
provision-remote: ssh-open-port
	ansible-playbook \
		--inventory-file "./inventory.ini" \
		"./provision.yml" \
		--connection "ssh" \
		--extra-vars "ansible_ssh_user=root" \
		--extra-vars "ansible_ssh_host=$(HOST_NAME)"


# SSH

COMMAND = bash -il

.PHONY: ssh-command
ssh-execute:
	sshpass -p "root" ssh -tt -o "StrictHostKeyChecking=no" -o "GlobalKnownHostsFile=/dev/null" -o "UserKnownHostsFile=/dev/null" "root@$(HOST_NAME)" $(COMMAND) || true

.PHONY: ssh-open-port
ssh-open-port:
	knock "$(HOST_NAME)" 3145:tcp 1414:tcp 2718:tcp

.PHONY: ssh-close-port
ssh-close-port:
	knock "$(HOST_NAME)" 2718:tcp 1414:tcp 3145:tcp

.PHONY: ssh
ssh: ssh-open-port ssh-execute ssh-close-port
