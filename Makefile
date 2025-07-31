# create icons
genicon:
	icon-gen -i ./icon_markrender.png -o icons

# create single file
onefile:
	rm -rf build dist
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	pyinstaller --upx-dir=./upx --onedir \
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
		--exclude-module "Pyside6.QtQuick" \
		--exclude-module "Pyside6.QtNetwork" \
		--exclude-module "Pyside6.QtDesigner" \
		--exclude-module "Pyside6.QtQuickWidgets" \
		--exclude-module "Pyside6.QtVirtualKeyboard" \
		--exclude-module "Pyside6.QtTextToSpeech" \
		--exclude-module "Pyside6.QtTest" \
		--exclude-module "Pyside6.QtSql" \
		--exclude-module "Pyside6.QtSpatialAudio" \
		--exclude-module "Pyside6.QtStateMachine" \
		--exclude-module "Pyside6.QtQuick3D" \
		--exclude-module "Pyside6.QtShaderTools" \
		--exclude-module "Pyside6.Qt3DCore" \
		--exclude-module "Pyside6.Qt3DRender" \
		--exclude-module "Pyside6.Qt3DInput" \
		--exclude-module "Pyside6.Qt3DLogic" \
		--exclude-module "Pyside6.Qt3DWindow" \
		--exclude-module "Pyside6.Qt3DAnimation" \
		--exclude-module "Pyside6.Qt3DExtras" \
		--exclude-module "Pyside6.QtScxml" \
		--exclude-module "Pyside6.QtQuickControls2" \
		--exclude-module "Pyside6.QtQuickTemplates2" \
		--exclude-module "Pyside6.QtQuickTest" \
		--exclude-module "Pyside6.QtQuick3DAnimation" \
		--exclude-module "Pyside6.QtQuick3DPhysics" \
		--exclude-module "Pyside6.QtQuick3DRender" \
		--exclude-module "Pyside6.QtQuick3DInput" \
		--exclude-module "Pyside6.QtQuick3DXr" \
		--exclude-module "Pyside6.QtQuick3DUtils" \
		--exclude-module "Pyside6.QtQuick3DAssetImport" \
		--exclude-module "Pyside6.QtQuick3DAssetUtils" \
		--exclude-module "Pyside6.QtQuick3DHelpers" \
		--exclude-module "Pyside6.QtQuick3DParticleEffects" \
		--exclude-module "Pyside6.QtQuick3DScene2D" \
		--exclude-module "Pyside6.QtQuickControls2Basic" \
		--exclude-module "Pyside6.QtQuickControls2Fluent" \
		--exclude-module "Pyside6.QtQuickControls2Material" \
		--exclude-module "Pyside6.QtQuickControls2Universal" \
		--exclude-module "Pyside6.QtQuickControls2Fusion" \
		--exclude-module "Pyside6.QtQuickControls2Imagine" \
		--exclude-module "Pyside6.QtQuickControls2Impl" \
		--exclude-module "Pyside6.QtQuickControls2Universal" \
		--exclude-module "Pyside6.QtQuickShapes" \
		--exclude-module "Pyside6.QtQuickEffects" \
		--exclude-module "Pyside6.QtSensors" \
		--exclude-module "Pyside6.QtSerialPort" \
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
