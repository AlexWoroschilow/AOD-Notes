project = CryptoNotes
project_version = 0.1
source_rpm = ~/rpmbuild/SOURCES
source_project = $(source_rpm)/$(project)-$(project_version)


all: appimage
	echo "done"

clean: 
	rm              -rf    $(project).AppDir
	rm              -rf    target/PyInstaller
	rm              -rf    target/$(project)


appimage:
	python3 		-m 		fbs freeze
	cp              -r     src/main/python/modules target/$(project)
	cp              -r     src/main/python/plugins target/$(project)
	cp              -r     src/main/python/template target/$(project)
	cp              -r     src/main/python/icons target/$(project)
	cp              -r     src/main/python/css target/$(project)
	cp              -r     src/main/python/lib target/$(project)
	cp              -r     src/main/python/application.py target/$(project)

	rm              -rf    $(project).AppDir
	mkdir           -p     $(project).AppDir/opt/$(project)
	cp              -r     target/$(project) $(project).AppDir/opt
	cp              -r     src/main/icons/Icon.svg $(project).AppDir/icon.svg
	echo			"[Desktop Entry]" >> $(project).AppDir/$(project).desktop
	echo			"Name=$(project)" >> $(project).AppDir/$(project).desktop
	echo			"Exec=AppRun" >> $(project).AppDir/$(project).desktop
	echo			"Icon=icon" >> $(project).AppDir/$(project).desktop
	echo			"Type=Application" >> $(project).AppDir/$(project).desktop
	echo			"Categories=Office;Education;" >> $(project).AppDir/$(project).desktop

	echo			"#! /bin/bash" >> $(project).AppDir/AppRun
	echo			"set -e" >> $(project).AppDir/AppRun
	echo			"cd \$${APPDIR}/opt/$(project)" >> $(project).AppDir/AppRun
	echo			"exec ./$(project)" >> $(project).AppDir/AppRun
	chmod 			+x $(project).AppDir/AppRun
	find 			$(project).AppDir -name '__pycache__' -exec rm -rf {} +
	find 			$(project).AppDir -name '.pyc*' -exec rm -rf {} +
	export 			ARCH=x86_64
	exec 			bin/appimagetool $(project).AppDir bin/CryptoNotes

