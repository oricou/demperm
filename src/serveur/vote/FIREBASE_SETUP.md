# Firebase Authentication Setup

This document describes how to configure Firebase authentication for the backend API.

## Overview

The backend uses Firebase Admin SDK to verify JWT tokens issued by Firebase Authentication on the frontend. The authentication flow is:

1. Frontend authenticates users via Firebase (email/password, Google, etc.)
2. Frontend receives a Firebase ID token (JWT)
3. Frontend calls any endpoint with the JWT in the Authorization header
4. Backend verifies the JWT using Firebase Admin SDK
5. If user doesn't exist in database, backend the user is created

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
demperm/
├── src/
│   └── serveur/
│       └── vote/
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
