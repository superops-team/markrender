import React from 'react';
import ReactDOM from 'react-dom/client';
import ExcalidrawBoard from './components/ExcalidrawBoard';
import './index.css';

// Add this line to properly import Excalidraw CSS
import '@excalidraw/excalidraw/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ExcalidrawBoard />
  </React.StrictMode>
);
