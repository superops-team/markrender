import React from 'react';
import ReactDOM from 'react-dom/client';
import TLDrawBoard from './components/TLDrawBoard';
import './index.css';

// 错误边界组件
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('[TLDraw] React错误边界捕获到错误:', error, errorInfo);
    
    // 报告错误到后端
    if (window.webChannelManager) {
      window.webChannelManager.sendToBackend('reportError', {
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack
      });
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          padding: '20px',
          textAlign: 'center',
          fontFamily: 'Arial, sans-serif'
        }}>
          <h1 style={{ color: '#dc3545' }}>❌ TLDraw 渲染错误</h1>
          <p>抱歉，TLDraw组件遇到了一个错误。</p>
          <details style={{ marginTop: '20px', textAlign: 'left' }}>
            <summary>错误详情</summary>
            <pre style={{ 
              background: '#f8f9fa', 
              padding: '10px', 
              borderRadius: '4px',
              maxWidth: '600px',
              overflow: 'auto'
            }}>
              {this.state.error?.message}
              {this.state.error?.stack && (
                <>\n\n堆栈跟踪:\n{this.state.error.stack}</>
              )}
            </pre>
          </details>
          <button 
            style={{
              marginTop: '20px',
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
            onClick={() => window.location.reload()}
          >
            🔄 重新加载页面
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <ErrorBoundary>
    <TLDrawBoard />
  </ErrorBoundary>
);