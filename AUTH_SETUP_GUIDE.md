# ScamShield Authentication Setup Guide

## Current Status
- ✅ Backend API: Working (`https://scamshield-api-hocl.onrender.com`)
- ✅ Registration: Working
- ✅ Login/Logout: Working
- ⚠️ Google OAuth: Needs configuration update on Render

---

## 🔧 REQUIRED: Update Render Environment Variables

Your backend uses the **wrong Google Client ID**. To fix Google OAuth:

### Step 1: Go to Render Dashboard
1. Visit https://dashboard.render.com
2. Select your **scamshield-api** service
3. Go to **Environment** tab

### Step 2: Update These Environment Variables

```
GOOGLE_CLIENT_ID=1064706061315-euungp6jbuki8tfhbaec9evlot75fqsr.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=https://scamshield-api-hocl.onrender.com/api/v1/auth/google/callback
```

### Step 3: Update Google Cloud Console
1. Go to https://console.cloud.google.com/apis/credentials
2. Select your OAuth 2.0 Client ID: `1064706061315-euungp6jbuki8tfhbaec9evlot75fqsr...`
3. Add these **Authorized redirect URIs**:
   - `https://scamshield-api-hocl.onrender.com/api/v1/auth/google/callback`
4. Add these **Authorized JavaScript origins**:
   - `https://scamshield-1gqy.vercel.app` (your Vercel frontend URL)
   - `https://scamshield-api-hocl.onrender.com`

### Step 4: Redeploy Backend
After updating environment variables, click **Manual Deploy** → **Deploy latest commit**

---

## Admin Credentials

```
Email: raghavshivam4321@gmail.com
Password: Thakur.4321
```

---

## API Endpoints Check

| Endpoint | Status |
|----------|--------|
| `GET /health` | ✅ Working |
| `POST /api/v1/auth/register` | ✅ Working |
| `POST /api/v1/auth/login` | ✅ Working |
| `POST /api/v1/auth/logout` | ✅ Working |
| `GET /api/v1/auth/google` | ⚠️ Needs correct Client ID |
| `POST /api/v1/auth/google/token` | ⚠️ Needs correct Client ID |

---

## Frontend Configuration

The frontend is correctly configured with:
- **API URL**: `https://scamshield-api-hocl.onrender.com`
- **Google Client ID**: `1064706061315-euungp6jbuki8tfhbaec9evlot75fqsr.apps.googleusercontent.com`

Files:
- `public-deploy/js/config.js`
- `public-deploy/js/auth.js`

---

## Troubleshooting

### "Google OAuth is not configured" error
→ `GOOGLE_CLIENT_ID` is missing in Render environment variables

### Login redirects back to login page
→ Check browser console for errors
→ Clear localStorage and try again

### Admin panel not accessible
→ Verify your account has `role: "admin"` in the database

### Session timeout too fast
→ `ACCESS_TOKEN_EXPIRE_MINUTES=30` (default)
→ Session management code adds 30-minute inactivity timeout in frontend
