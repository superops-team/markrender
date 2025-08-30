// TypeScript declarations for window objects
declare global {
  interface Window {
    // For webchannel-core.js
    WebChannelManager?: {
      initWebChannel: (pageType: string) => Promise<void>;
      registerMessageHandler: (action: string, handler: Function) => void;
      unregisterMessageHandler: (action: string) => void;
      sendToPython: (action: string, data: any) => Promise<any>;
    };
    
    // For error reporting
    webChannelManager?: {
      sendToPython: (action: string, data: any) => void;
    };
  }
}

export {}