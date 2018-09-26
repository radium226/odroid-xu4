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
