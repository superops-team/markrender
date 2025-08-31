import './polyfills.js';
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// 移除 React.StrictMode 以避免 Excalidraw 的双重渲染问题
ReactDOM.createRoot(document.getElementById('root')).render(
  <App />
)