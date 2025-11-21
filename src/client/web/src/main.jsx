import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'

// Only load MSW in development (never in production)
if (import.meta.env.DEV) {
  import('./tests/mock')
    .then(({ worker }) => worker.start())
    .catch((err) => console.error('Failed to start MSW', err))
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)
