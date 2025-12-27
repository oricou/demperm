import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'

// Only load MSW when explicitly enabled (keeps real API usable in dev).
if (import.meta.env.DEV) {
  const enableMocks = import.meta.env.VITE_ENABLE_MOCKS === 'true'
  if (enableMocks) {
    import('./tests/mock')
      .then(({ worker }) => worker.start({ onUnhandledRequest: 'bypass' }))
      .catch((err) => console.error('Failed to start MSW', err))
  } else if ('serviceWorker' in navigator) {
    // If MSW was enabled in a previous session, unregister it so it doesn't keep intercepting requests.
    navigator.serviceWorker
      .getRegistrations()
      .then((registrations) =>
        Promise.all(
          registrations
            .filter((registration) => registration.active?.scriptURL?.includes('mockServiceWorker.js'))
            .map((registration) => registration.unregister())
        )
      )
      .catch(() => {})
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)
