# 生成单文件
onefile:
	rm -rf build dist
	pyinstaller --onedir --windowed  --hidden-import="PySide6.QtXml" --hidden-import="PySide6.QtSvg" --hidden-import="PySide6.QtNetwork" --name "markrender" --icon "./icons/app.icns" *.py

# 创建 dmg
dmg: onefile
	mkdir -p dist/dmg
	mv dist/markrender.app dist/dmg
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
 	  
# 格式化代码
fmt:
	autopep8 --in-place --recursive --aggressive --aggressive .