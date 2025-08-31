declare global {
  interface Window {
    // For webchannel-core.js
    WebChannelManager?: {
      initWebChannel: (pageType: string) => Promise<void>;
      registerMessageHandler: (action: string, handler: Function) => void;
      unregisterMessageHandler: (action: string) => void;
      sendToPython: (action: string, data: any) => Promise<any>;
    };
  }
}

export {}