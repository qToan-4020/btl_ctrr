// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx' // Đảm bảo dòng này trỏ đúng vào App.tsx
import './index.css' // Nếu bạn không dùng css thì xóa dòng này đi cũng được

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)