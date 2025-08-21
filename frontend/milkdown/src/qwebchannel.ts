declare global {
  interface Window {
    qt: any;
    QWebChannel: any;
  }
}

export function setupQWebChannel(): Promise<any> {
  return new Promise((resolve) => {
    if (window.qt && window.QWebChannel) {
      new window.QWebChannel(window.qt.webChannelTransport, (channel: any) => {
        resolve(channel.objects.markdownBridge);
      });
    } else {
      resolve(null);
    }
  });
}