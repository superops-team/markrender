import { b as createRoot, R as React, m as mainExports } from "./main.3994856f.js";
let excalidrawAPI = null;
function getContent() {
  console.log("getContent called");
  if (!excalidrawAPI) {
    console.warn("Excalidraw 尚未初始化");
    return null;
  }
  const elements = excalidrawAPI.getSceneElements();
  const appState = excalidrawAPI.getAppState();
  return {
    elements,
    appState
  };
}
function setValue(content) {
  console.log("setValue called", content);
  if (!excalidrawAPI) {
    console.warn("Excalidraw 尚未初始化");
    return;
  }
  if (content && content.elements) {
    excalidrawAPI.updateScene({
      elements: content.elements,
      appState: content.appState || {},
      commitToHistory: true
    });
  }
}
function reset() {
  console.log("reset called");
  if (!excalidrawAPI) {
    console.warn("Excalidraw 尚未初始化");
    return;
  }
  excalidrawAPI.resetScene();
}
window.getContent = getContent;
window.setValue = setValue;
window.reset = reset;
console.log("Functions exposed to window object");
console.log("getContent function available:", typeof window.getContent === "function");
console.log("setValue function available:", typeof window.setValue === "function");
console.log("reset function available:", typeof window.reset === "function");
function initializeExcalidraw() {
  console.log("Initializing Excalidraw...");
  const container = document.getElementById("excalidraw-container");
  console.log("Container element:", container);
  if (!container) {
    console.error("Container element not found");
    return;
  }
  const root = createRoot(container);
  console.log("Root created");
  try {
    const excalidrawElement = React.createElement(mainExports.Excalidraw, {
      onChange: (elements, state) => {
        console.log("Excalidraw elements changed", elements.length);
      },
      onMount: (api) => {
        console.log("Excalidraw mounted, API received:", typeof api);
        excalidrawAPI = api;
        console.log("Excalidraw API stored:", typeof excalidrawAPI);
        console.log("Excalidraw 初始化完成");
        console.log("getContent function available:", typeof window.getContent === "function");
        console.log("setValue function available:", typeof window.setValue === "function");
        console.log("reset function available:", typeof window.reset === "function");
        if (excalidrawAPI) {
          console.log("Testing API...");
          try {
            const elements = excalidrawAPI.getSceneElements();
            console.log("API test successful, elements count:", elements.length);
          } catch (e) {
            console.error("API test failed:", e);
          }
        }
      }
    });
    root.render(excalidrawElement);
    console.log("Excalidraw rendered");
  } catch (error) {
    console.error("Error rendering Excalidraw:", error);
  }
}
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM content loaded, initializing Excalidraw...");
  setTimeout(() => {
    initializeExcalidraw();
  }, 100);
});
window.addEventListener("load", () => {
  console.log("Window loaded, initializing Excalidraw...");
  setTimeout(() => {
    initializeExcalidraw();
  }, 100);
});
