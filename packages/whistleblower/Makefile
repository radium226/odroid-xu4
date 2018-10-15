./.venv:
	virtualenv \
		--system-site-packages \
		"./.venv"

.PHONY: install
install: install-requirements
	pip install --editable "."

.PHONY: install-requirements
install-requirements:
	if ! yay -Q "python-gobject"; then \
		yay -S "python-gobject" --noconfirm ; \
	fi
	pip install --requirement "./requirements.txt"

.PHONY: clean
clean:
	rm -Rf "./.venv" || true

.PHONY: develop
develop: ./.venv
	bash \
		--rcfile "./.bashrc" \
		-i
