import './App.css'
import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { isAuthenticated, clearCredentials } from './shared/auth'
import Login from './app/auth/login'
import { AppShell } from './components/layout/AppShell'
import ProfileSelfPage from './app/social/dashboard/page'
import PublicProfilePage from './app/social/users/id'
import CreateProfilePage from './app/social/users/create'
import VoteDashboardPage from './app/vote/page'
import ForumHomePage from './app/social/groups'
import MessagesPage from './app/social/mailbox'
import { GlobalProfileSearch } from './components/GlobalProfileSearch'

function AppLayout() {
  return (
    <AppShell>
      <Outlet />
    </AppShell>
  )
}

function RequireAuth({ children }) {
  const ok = typeof window !== 'undefined' && isAuthenticated()
  if (!ok) {
    if (typeof window !== 'undefined') clearCredentials()
    return <Navigate to="/login" replace />
  }
  return children
}

function App() {
  return (

    <>
      <Routes>
        <Route path="/" element={<Navigate to="/profil" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/auth/login" element={<Login />} />
        <Route element={<RequireAuth><AppLayout /></RequireAuth>}>
          <Route path="/profil" element={<ProfileSelfPage />} />
          <Route path="/profil/public" element={<PublicProfilePage />} />
          <Route path="/vote" element={<VoteDashboardPage />} />
          <Route path="/forum" element={<ForumHomePage />} />
          <Route path="/messages" element={<MessagesPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/profil" replace />} />
      </Routes>
      <GlobalProfileSearch />
    </>
// next is from client-web branch
//    <Routes>
//       <Route path="/" element={<Navigate to="/profil" replace />} />
//       <Route path="/login" element={<Login />} />
//       <Route path="/auth/login" element={<Login />} />
//       <Route element={<RequireAuth><AppLayout /></RequireAuth>}>
//         <Route path="/profil" element={<ProfileSelfPage />} />
//         <Route path="/profil/create" element={<CreateProfilePage />} />
//         <Route path="/profil/public" element={<PublicProfilePage />} />
//         <Route path="/vote" element={<VoteDashboardPage />} />
//         <Route path="/forum" element={<ForumHomePage />} />
//         <Route path="/messages" element={<MessagesPage />} />
//       </Route>
//       <Route path="*" element={<Navigate to="/profil" replace />} />
//     </Routes>

  )
}

export default App
