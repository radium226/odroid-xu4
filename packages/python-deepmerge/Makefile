ARCHIVE_FOLDER_PATH = .
.PHONY:

.PHONY: pypi2pkgbuild
pypi2pkgbuild:
	if [[ ! -d "./python-deepmerge" ]]; then \
		pypi2pkgbuild.py \
			--no-install \
			--base-path="." \
			"deepmerge" ; \
	fi


.PHONY: copy-pkgbuild
copy-pkgbuild: pypi2pkgbuild
	cp "./python-deepmerge/PKGBUILD" "."
	cp "./python-deepmerge/PKGBUILD_EXTRAS" "."
	cp "./python-deepmerge/LICENSE" "."

.PHONY: makepkg
makepkg: copy-pkgbuild
	makepkg

.PHONY: package
package: makepkg
	if [[ "$(ARCHIVE_FOLDER_PATH)" != "." ]]; then \
		find "." -name "*.pkg.tar.xz" -mindepth 1 -maxdepth=1 | \
			xargs -I {} cp "{}" "$(ARCHIVE_FOLDER_PATH)" ; \
	fi


.PHONY: clean
clean:
	rm -Rf "./python-deepmerge" || true
	rm -Rf "./PKGBUILD" || true
	rm -Rf "./PKGBUILD_EXTRAS" || true
	rm -Rf "./LICENSE" || true
	rm -Rf "./src" || true
	rm -Rf "./pkg" || true
	{ find "." -name "*.pkg.tar.xz" | xargs -I {} rm "{}" ; } || true
	{ find "." -name "*.whl" | xargs -I {} rm "{}" ; } || true
