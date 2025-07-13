# create icons
genicon:
	icon-gen -i ./icon_markrender.png -o icons

# create single file
onefile:
	rm -rf build dist
	pyinstaller --onedir \
		--clean \
		--windowed  \
		--name "markrender" \
		--icon "./icons/app.icns" \
		--add-data "icons/app.icns:." \
		--add-data "icons:icons" \
		--add-data "app/editor/resources:app/editor/resources" \
		--hidden-import "scipy" \
		--hidden-import "scipy._cyutility" \
		--hidden-import "numpy" \
		--noconfirm \
		main.py

# create dmg
dmg: onefile
	mkdir -p dist/dmg
	mv dist/markrender.app dist/dmg

	create-dmg \
	  --volname "markrender" \
	  --volicon "icons/app.icns" \
	  --window-pos 200 120 \
	  --window-size 600 300 \
	  --icon-size 90 \
	  --icon "markrender.app" 120 100 \
	  --hide-extension "markrender.app" \
	  --app-drop-link 425 120 \
	  "dist/markrender.dmg" \
	  "dist/dmg/"
 	  
# format all python files
fmt:
	autopep8 --in-place --recursive --aggressive --aggressive .

# clean no used files
clean:
	rm -rf app.log config.db build dist