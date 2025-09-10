import { r as requireJsxRuntime, a as reactExports, m as mainExports, c as client } from "./main.3994856f.js";
var jsxRuntimeExports = requireJsxRuntime();
const index = "";
function App() {
  const [excalidrawAPI, setExcalidrawAPI] = reactExports.useState(null);
  const handleExcalidrawMount = (api) => {
    console.log("Excalidraw mounted with API:", !!api);
    setExcalidrawAPI(api);
    if (api) {
      window.setValue = (sceneData) => {
        console.log("setValue called with:", sceneData);
        if (sceneData) {
          api.updateScene(sceneData);
        }
      };
      window.reset = () => {
        console.log("reset called");
        api.resetScene();
      };
      window.getContent = () => {
        console.log("getContent called");
        return {
          elements: api.getSceneElements(),
          appState: api.getAppState(),
          files: api.getFiles()
        };
      };
      window.getCurrentItemId = () => {
        console.log("getCurrentItemId called");
        return "default-item-id";
      };
      window.setCurrentItemId = (itemId) => {
        console.log("setCurrentItemId called with:", itemId);
      };
      console.log("Excalidraw API exposed to window");
      console.log("Available functions:", {
        getContent: typeof window.getContent,
        setValue: typeof window.setValue,
        reset: typeof window.reset,
        getCurrentItemId: typeof window.getCurrentItemId,
        setCurrentItemId: typeof window.setCurrentItemId
      });
    }
  };
  const handleExcalidrawChange = (elements, appState, files) => {
    console.log("Excalidraw changed");
  };
  return /* @__PURE__ */ jsxRuntimeExports.jsx("div", { style: { height: "100vh" }, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
    mainExports.Excalidraw,
    {
      excalidrawAPI: handleExcalidrawMount,
      onChange: handleExcalidrawChange
    }
  ) });
}
const root = client.createRoot(document.getElementById("excalidraw-container"));
root.render(
  /* @__PURE__ */ jsxRuntimeExports.jsx(App, {})
);
