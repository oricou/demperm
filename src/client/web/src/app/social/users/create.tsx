import { useState, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { Box, Card, CardContent, CardHeader, TextField, FormControlLabel, Checkbox, Alert, Button, Typography } from '@mui/material'
import { apiClient } from '../../../domains/vote/api/apiClient'
import { getCredentials, setUser } from '../../../shared/auth'

export default function CreateProfilePage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [bio, setBio] = useState('')
  const [location, setLocation] = useState('FR')
  const [isPrivate, setIsPrivate] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)

    const { token } = getCredentials()
    if (!token) {
      setError("Token Firebase manquant. Merci de vous reconnecter.")
      return
    }

    if (!username.trim()) {
      setError('Le pseudo est obligatoire')
      return
    }

    setLoading(true)
    try {
      const payload = await apiClient.post<any, any>('/api/v1/users/', {
        username: username.trim(),
        bio: bio.trim() || null,
        location: location.trim() || null,
        // Backend expects a boolean: True = public, False = private
        privacy: !isPrivate,
      })

      setUser(payload)
      navigate('/profil', { replace: true })
    } catch (err: any) {
      const message = err?.message || "Erreur lors de la création du profil"
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box display="flex" justifyContent="center" mt={4}>
      <Card sx={{ maxWidth: 600, width: '100%' }}>
        <CardHeader
          title={<Typography variant="h6">Créer votre profil</Typography>}
          subheader="Complétez quelques informations pour finaliser votre compte."
        />
        <CardContent>
          <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
            <TextField
              label="Pseudo"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              fullWidth
            />
            <TextField
              label="Bio"
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              fullWidth
              multiline
              minRows={3}
            />
            <TextField
              label="Localisation"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              fullWidth
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={isPrivate}
                  onChange={(e) => setIsPrivate(e.target.checked)}
                />
              }
              label="Profil privé"
            />

            {error && (
              <Alert severity="error">{error}</Alert>
            )}

            <Button type="submit" variant="contained" color="primary" disabled={loading}>
              {loading ? 'Création en cours…' : 'Créer mon profil'}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  )
}
