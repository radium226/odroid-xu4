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
	python "./setup.py" clean
	rm -Rf "./dist" || true
	rm -Rf "./$(NAME)-$(VERSION).tar.gz" || true
	rm -Rf "./pkg" || true
	find . -name "*.pkg.tar.xz" | xargs -I {} rm "{}" || true
	rm -Rf "./src" || true
	rm -Rf "whistleblower.egg-info" || true

.PHONY: develop
develop: ./.venv
	bash \
		--rcfile "./.bashrc" \
		-i

NAME = $(shell basename "$(PWD)")
VERSION = $(shell cat "./VERSION.txt")
RELEASE = $(shell echo $(shell pacman -Si "$(NAME)" 2>"/dev/null" || echo "Version 0:0" | tr -d ' ' | grep '^Version' | cut -d':' -f2 | cut -d'-' -f2) + 1 | bc )
ARCHIVE_FOLDER_PATH = .

.PHONY: debug
debug:
	@echo "NAME=$(NAME)"
	@echo "VERSION=$(VERSION)"
	@echo "RELEASE=$(RELEASE)"

./dist/$(NAME)-$(VERSION).tar.gz:
	python "./setup.py" sdist --format="gztar"

./$(NAME)-$(VERSION).tar.gz: ./dist/$(NAME)-$(VERSION).tar.gz
	cp "./dist/$(NAME)-$(VERSION).tar.gz" "./$(NAME)-$(VERSION).tar.gz"

package: $(NAME)-$(VERSION).tar.gz
	PKGNAME="$(NAME)" \
	PKGVER="$(VERSION)" \
	PKGREL="$(RELEASE)" \
		makepkg \
			--force \
			--skipchecksums \
			--nodeps
	if [[ "$(ARCHIVE_FOLDER_PATH)" != "." ]]; then \
		find . -name "*.pkg.tar.xz" | xargs -I {} cp "{}" "$(ARCHIVE_FOLDER_PATH)" ; \
	fi
