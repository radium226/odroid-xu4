./.venv:
	virtualenv "./.venv"

.PHONY: virtualenv-activate
virtualenv-activate: ./.venv
	bash \
		--rcfile "./bashrc" \
		-i

.PHONY: pip-install-editable
pip-install-editable:
	pip install --editable "."

.PHONY: clean
clean: pacman-clean
	rm -Rf "./.venv" || true

.PHONY: pacman-package
pacman-package:
	make -f "./Makefile.pacman" package

.PHONY: pacman-clean
pacman-clean:
	make -f "./Makefile.pacman" clean

ARCHIVE_FOLDER_PATH = .
.PHONY: package
package: pacman-package
	find . -name "*.pkg.tar.xz" | xargs -I {} cp "{}" "$(ARCHIVE_FOLDER_PATH)"

.PHONY: pacman-install
pacman-install:
	make -f "Makefile.pacman" install

.PHONY: install
install: pacman-install
