import { setupWorker } from 'msw/browser'

// Import the handlers of each feature/domain
import { authHandlers } from './handlers/auth'
import { userHandlers } from './handlers/users'
import { dashboardHandlers } from './handlers/dashboard'
import { communityHandlers } from './handlers/communities'
import { chatHandlers } from './handlers/chats'

/**
 * The MSW (Mock Service Worker) instance.
 * It intercepts network requests at the browser level
 * and returns mocked responses instead of calling a real API.
 */
export const worker = setupWorker(
  ...authHandlers,
  ...userHandlers,
  ...dashboardHandlers,
  ...communityHandlers,
  ...chatHandlers
)

// The worker only runs in development mode.
// In production, the real API must be used.
if (process.env.NODE_ENV === 'development') {
  worker.start({
    onUnhandledRequest: 'bypass', // Avoid warnings for requests not mocked
  })
}
