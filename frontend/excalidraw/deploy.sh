#!/bin/bash

npm run build

cp dist/index.html ../../app/editor/plugins/excalidraw/index.html
cp dist/assets/* ../../app/editor/plugins/excalidraw/assets
