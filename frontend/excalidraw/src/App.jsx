import React from 'react'
import { Excalidraw } from "@excalidraw/excalidraw";
import "./App.css";

// 在组件定义之前就设置 Excalidraw 的资源路径
if (typeof window !== 'undefined') {
  // 确保 Excalidraw 使用本地资源而不是 CDN
  // 注意：路径末尾必须包含斜杠，但不能有重复路径
  window.EXCALIDRAW_ASSET_PATH = "./assets/";
  window.EXCALIDRAW_EXPORT_SOURCE = "";
}

function App() {
  const onChange = (elements, state) => {
    console.log("Elements changed", elements, state);
  };

  return (
    <div className="App">
      <div className="excalidraw-wrapper">
        <Excalidraw 
          onChange={onChange}
          // 确保不使用 CDN
          UIOptions={{
            canvasActions: {
              export: {
                saveFileToDisk: true
              }
            }
          }}
        />
      </div>
    </div>
  );
}

export default App;