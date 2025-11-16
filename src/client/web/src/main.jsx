import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Only load MSW in development (never in production)
if (process.env.NODE_ENV === 'development') {
  import('./tests/mock')
    .then(({ worker }) => worker.start())
    .catch((err) => console.error('Failed to start MSW', err))
}

// Existing imports
import React from 'react'
import ReactDOM from 'react-dom/client'

// Your existing render logic
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
