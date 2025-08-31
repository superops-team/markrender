// 添加浏览器环境所需的 polyfills
(function () {
  if (typeof window !== 'undefined') {
    // 设置 global
    window.global = window;
    
    // 设置 process
    if (!window.process) {
      window.process = {
        env: {},
        platform: 'browser'
      };
    } else {
      if (!window.process.env) {
        window.process.env = {};
      }
      if (!window.process.platform) {
        window.process.platform = 'browser';
      }
    }
    
    // 设置 globalThis
    window.globalThis = window;
  }
})();