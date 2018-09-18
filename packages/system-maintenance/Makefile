./.venv:
	virtualenv "./.venv"

.PHONY: virtualenv-activate
virtualenv-activate: ./.venv
	bash \
		--rcfile "./bashrc" \
		-i

.PHONY: upgrade-packages
upgrade-packages:
	python -m "system.maintenance" "upgrade-packages"

.PHONY: pip-install-editable
pip-install-editable:
	pip install --editable "."

.PHONY: link-systemd-files
link-systemd-files:
	mkdir -p "${HOME}/.config/systemd/user" || true
	ln "./package-upgrade.service" "${HOME}/.config/systemd/user" || true
	ln "./package-upgrade.timer" "${HOME}/.config/systemd/user" || true
	mkdir -p "${HOME}/.config/systemd/user/package-upgrade.service.d" || true
	echo '[Service]' >"${HOME}/.config/systemd/user/package-upgrade.service.d/virtualenv.conf"
	echo 'ExecStart=' >>"${HOME}/.config/systemd/user/package-upgrade.service.d/virtualenv.conf"
	echo 'ExecStart=bash -c "source $(PWD)/.venv/bin/activate ; python -m yay.jobs -- upgrade-packages"' >>"${HOME}/.config/systemd/user/package-upgrade.service.d/virtualenv.conf"
	systemctl --user daemon-reload
	systemctl --user start package-upgrade.timer

.PHONY: systemctl-list-timers
systemctl-list-timers:
	systemctl --user list-timers

.PHONY: systemctl-show
systemctl-show:
	systemctl --user show "package-upgrade.service"

.PHONY: systemctl-status
systemctl-status:
	systemctl --user status "package-upgrade.service"

.PHONY: journalctl
journalctl:
	journalctl --user --unit "package-upgrade.service" -e

.PHONY: clean
clean:
	rm -Rf "./.venv" || true
	systemctl --user stop "package-upgrade.timer" || true
	rm "${HOME}/.config/systemd/system/user/package-upgrade.service" || true
	rm "${HOME}/.config/systemd/system/user/package-upgrade.timer" || true
	rm -Rf "${HOME}/.config/systemd/system/user/package-upgrade.d" || true
	systemctl --user daemon-reload

.PHONY: pacman-package:
	make -f "./Makefile.pacman" package

ARCHIVE_FOLDER_PATH = .
.PHONY: package
package: pacman-package
	find . -name "*.pkg.tar.xz" | xargs -I {} cp "{}" "$(ARCHIVE_FOLDER_PATH)"
