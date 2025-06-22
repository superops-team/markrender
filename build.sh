#!/bin/bash
# 生成各种图标
# icon-gen -i ./shen_1179.png -o icons
rm -rf build dist
# 创建安装包
pyinstaller --onefile --windowed --add-data ./config.db --hidden-import="PySide6.QtXml" --hidden-import="PySide6.QtSvg" --hidden-import="PySide6.QtNetwork" --name "markrender" --icon "./icons/app.icns" *.py
mkdir -p dist/dmg
cp -r "dist/markrender.app" dist/dmg

create-dmg \
  --volname "markrender" \
  --volicon "icons/app.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "markrender.app" 175 120 \
  --hide-extension "markrender.app" \
  --app-drop-link 425 120 \
  "dist/markrender.dmg" \
  "dist/dmg/"
