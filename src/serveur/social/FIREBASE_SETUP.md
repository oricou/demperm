# Firebase Authentication Setup

This document describes how to configure Firebase authentication for the backend API.

## Overview

The backend uses Firebase Admin SDK to verify JWT tokens issued by Firebase Authentication on the frontend. The authentication flow is:

1. Frontend authenticates users via Firebase (email/password, Google, etc.)
2. Frontend receives a Firebase ID token (JWT)
3. Frontend calls `GET /api/v1/users/me` with the JWT in the Authorization header
4. Backend verifies the JWT using Firebase Admin SDK
5. If user doesn't exist in database, backend returns `null`
6. Frontend then calls `POST /api/v1/users/` to create the user account
7. Subsequent requests use the same Firebase JWT for authentication

## Configuration Steps

### 1. Get Firebase Service Account Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Project Settings** (gear icon) > **Service Accounts**
4. Click **Generate New Private Key**
5. Download the JSON file (e.g., `firebase-service-account.json`)
6. **Keep this file secure!** Never commit it to version control

### 2. Configure Environment Variables

Add the following to your `.env` file:

```bash
# Firebase Configuration
FIREBASE_SERVICE_ACCOUNT_KEY=/path/to/firebase-service-account.json
```

**Note**: If you're running on Google Cloud Platform (App Engine, Cloud Run, etc.), you can omit this variable and Firebase will use Application Default Credentials automatically.

### 3. Place Service Account Key

Place the downloaded JSON file in a secure location on your server. The path should match the environment variable you set.

**Example structure:**
```
/home/maxsa/epita/geopo/demperm-social/
├── src/
│   └── serveur/
│       └── social/
│           ├── api/
│           ├── firebase-service-account.json  # NOT in git!
│           └── ...
```

### 4. Update .gitignore

Make sure your `.gitignore` includes:

```
# Firebase
firebase-service-account.json
*-firebase-adminsdk-*.json
```

## API Endpoints

### Check Current User (GET /api/v1/users/me)

Returns the current user's profile, or `null` if authenticated but not registered.

**Request:**
```http
GET /api/v1/users/me
Authorization: Bearer <firebase-id-token>
```

**Response (user exists):**
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "is_admin": false,
  "is_banned": false,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login_at": "2024-01-15T10:30:00Z",
  "profile": {
    "display_name": "John Doe",
    "profile_picture_url": "https://...",
    "bio": "Hello!",
    "location": "Paris",
    "privacy": "public"
  },
  "settings": {
    "email_notifications": true,
    "language": "fr"
  }
}
```

**Response (user authenticated but not in database):**
```json
null
```

**Response (not authenticated):**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

### Create User (POST /api/v1/users/)

Creates a new user account for an authenticated Firebase user.

**Request:**
```http
POST /api/v1/users/
Authorization: Bearer <firebase-id-token>
Content-Type: application/json

{
  "username": "johndoe",
  "display_name": "John Doe",
  "profile_picture_url": "https://...",
  "bio": "Hello world!",
  "location": "Paris",
  "privacy": "public",
  "email_notifications": true,
  "language": "fr"
}
```

**Required fields:**
- `username`: 3-50 characters, alphanumeric with `_` or `-`

**Optional fields:**
- `display_name`: Display name (defaults to username)
- `profile_picture_url`: Profile picture URL
- `bio`: User bio (max 500 characters)
- `location`: User location
- `privacy`: "public" or "private" (default: "public")
- `email_notifications`: Boolean (default: true)
- `language`: "fr" or "en" (default: "fr")

**Response (success):**
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "is_admin": false,
  "is_banned": false,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login_at": null,
  "profile": {
    "display_name": "John Doe",
    "profile_picture_url": "https://...",
    "bio": "Hello world!",
    "location": "Paris",
    "privacy": "public"
  },
  "settings": {
    "email_notifications": true,
    "language": "fr"
  }
}
```

**Response (user already exists):**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "User already registered"
  }
}
```

## Frontend Integration

### Example Flow

```javascript
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';

// 1. Sign in with Firebase
const auth = getAuth();
const userCredential = await signInWithEmailAndPassword(auth, email, password);
const idToken = await userCredential.user.getIdToken();

// 2. Check if user exists in backend
const meResponse = await fetch('https://api.example.com/api/v1/users/me', {
  headers: {
    'Authorization': `Bearer ${idToken}`
  }
});

const userData = await meResponse.json();

// 3. If user doesn't exist (null response), create user
if (userData === null) {
  const createResponse = await fetch('https://api.example.com/api/v1/users/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${idToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: 'johndoe',
      display_name: 'John Doe',
      privacy: 'public'
    })
  });
  
  const newUser = await createResponse.json();
  console.log('User created:', newUser);
} else {
  console.log('User exists:', userData);
}
```

### Token Refresh

Firebase ID tokens expire after 1 hour. The frontend should refresh tokens periodically:

```javascript
import { getAuth } from 'firebase/auth';

const auth = getAuth();
const user = auth.currentUser;

if (user) {
  // Force refresh token
  const idToken = await user.getIdToken(true);
  
  // Use refreshed token for API calls
}
```

## Database Migration

After setting up Firebase authentication, you need to create a database migration for the new `firebase_uid` field:

```bash
cd /home/maxsa/epita/geopo/demperm-social/src/serveur/social/api
python manage.py makemigrations
python manage.py migrate
```

## Security Considerations

1. **Never expose service account keys**: Keep `firebase-service-account.json` secure and never commit it to version control
2. **Use HTTPS**: Always use HTTPS in production to protect JWT tokens in transit
3. **Token expiration**: Firebase ID tokens expire after 1 hour. Frontend must handle token refresh
4. **Validate tokens**: The backend always validates tokens using Firebase Admin SDK before trusting any claims
5. **Firebase UID is immutable**: The `firebase_uid` uniquely identifies each user and never changes

## Troubleshooting

### "Invalid Firebase token" error

- Check that the token is a valid Firebase ID token (not a custom token or refresh token)
- Ensure the token hasn't expired (tokens expire after 1 hour)
- Verify the service account key matches your Firebase project

### "Firebase authentication failed" error

- Check that `FIREBASE_SERVICE_ACCOUNT_KEY` environment variable is set correctly
- Verify the service account JSON file exists at the specified path
- Ensure the service account has proper permissions in Firebase Console

### "User already registered" when creating user

- The Firebase UID is already associated with a user in the database
- Use `GET /api/v1/users/me` to retrieve the existing user

## Development vs Production

### Development

In development, use the service account key file:

```bash
FIREBASE_SERVICE_ACCOUNT_KEY=/path/to/firebase-service-account.json
```

### Production (Google Cloud Platform)

On GCP, you can use Application Default Credentials. Simply omit the `FIREBASE_SERVICE_ACCOUNT_KEY` variable and ensure your service account has the necessary Firebase permissions:

```bash
# No FIREBASE_SERVICE_ACCOUNT_KEY needed on GCP
```

The Firebase Admin SDK will automatically use the service account associated with your App Engine, Cloud Run, or Compute Engine instance.

## Additional Resources

- [Firebase Admin SDK Setup](https://firebase.google.com/docs/admin/setup)
- [Verify ID Tokens](https://firebase.google.com/docs/auth/admin/verify-id-tokens)
- [Firebase Authentication](https://firebase.google.com/docs/auth)
