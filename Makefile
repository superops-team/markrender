# create icons
genicon:
	icon-gen -i ./icon_markrender.png -o icons --icns  --icns-sizes 16,32,64,128,256,512,1024


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
		--noconfirm \
		--hidden-import "numpy" \
		--exclude-module "PyQt5" \
		--exclude-module "test" \
		--exclude-module "tests" \
		--exclude-module "unittest" \
		--exclude-module "matplotlib" \
		--exclude-module "PySide6.QtQuick" \
		--exclude-module "PySide6.QtDesigner" \
		--exclude-module "PySide6.QtQuickWidgets" \
		--exclude-module "PySide6.QtVirtualKeyboard" \
		--exclude-module "PySide6.QtTextToSpeech" \
		--exclude-module "PySide6.QtTest" \
		--exclude-module "PySide6.QtSql" \
		--exclude-module "PySide6.QtSpatialAudio" \
		--exclude-module "PySide6.QtStateMachine" \
		--exclude-module "PySide6.QtQuick3D" \
		--exclude-module "PySide6.QtShaderTools" \
		--exclude-module "PySide6.Qt3DCore" \
		--exclude-module "PySide6.Qt3DRender" \
		--exclude-module "PySide6.Qt3DInput" \
		--exclude-module "PySide6.Qt3DLogic" \
		--exclude-module "PySide6.Qt3DWindow" \
		--exclude-module "PySide6.Qt3DAnimation" \
		--exclude-module "PySide6.Qt3DExtras" \
		--exclude-module "PySide6.QtScxml" \
		--exclude-module "PySide6.QtQuickControls2" \
		--exclude-module "PySide6.QtQuickTemplates2" \
		--exclude-module "PySide6.QtQuickTest" \
		--exclude-module "PySide6.QtQuick3DAnimation" \
		--exclude-module "PySide6.QtQuick3DPhysics" \
		--exclude-module "PySide6.QtQuick3DRender" \
		--exclude-module "PySide6.QtQuick3DInput" \
		--exclude-module "PySide6.QtQuick3DXr" \
		--exclude-module "PySide6.QtQuick3DUtils" \
		--exclude-module "PySide6.QtQuick3DAssetImport" \
		--exclude-module "PySide6.QtQuick3DAssetUtils" \
		--exclude-module "PySide6.QtQuick3DHelpers" \
		--exclude-module "PySide6.QtQuick3DParticleEffects" \
		--exclude-module "PySide6.QtQuick3DScene2D" \
		--exclude-module "PySide6.QtQuickControls2Basic" \
		--exclude-module "PySide6.QtQuickControls2Fluent" \
		--exclude-module "PySide6.QtQuickControls2Material" \
		--exclude-module "PySide6.QtQuickControls2Universal" \
		--exclude-module "PySide6.QtQuickControls2Fusion" \
		--exclude-module "PySide6.QtQuickControls2Imagine" \
		--exclude-module "PySide6.QtQuickControls2Impl" \
		--exclude-module "PySide6.QtQuickControls2Universal" \
		--exclude-module "PySide6.QtQuickShapes" \
		--exclude-module "PySide6.QtQuickEffects" \
		--exclude-module "PySide6.QtSensors" \
		--exclude-module "PySide6.QtSerialPort" \
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
	  --icon "markrender.app" 175 120 \
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
