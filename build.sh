#!/bin/bash
# 生成各种图标
# icon-gen -i ./shen_1179.png -o icons

rm -rf build dist
# 创建安装包
pyinstaller --onedir \
		--clean \
		--windowed  \
		--name "markrender" \
		--icon "./icons/app.icns" \
		--add-data "icons/app.icns:." \
		--add-data "icons:icons" \
		--add-data "app/editor/resources:app/editor/resources" \
		--add-data "ui/assets:ui/assets" \
		--hidden-import "PyQt5" \
		main.py

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
