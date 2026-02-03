# 🚀 Free Deployment Guide for ScamShield

This guide will help you deploy ScamShield for **FREE** using:
- **Frontend**: Netlify (free tier)
- **Backend**: Render.com (free tier)
- **Database**: MongoDB Atlas (free 512MB cluster)

---

## 📋 Prerequisites

- GitHub account (free)
- Your project pushed to GitHub

---

## Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scamshield.git
git push -u origin main
```

---

## Step 2: Set Up MongoDB Atlas (Free Database)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create a free account
3. Create a **FREE** shared cluster (M0 tier)
4. Choose any region (closest to you)
5. Wait for cluster to be created (~2-3 minutes)

### Configure Database Access:
1. Go to **Database Access** → **Add New Database User**
2. Create a username and password (save these!)
3. Set privileges to **Read and write to any database**

### Configure Network Access:
1. Go to **Network Access** → **Add IP Address**
2. Click **Allow Access from Anywhere** (0.0.0.0/0)
   - ⚠️ This is okay for free tier, but restrict for production

### Get Connection String:
1. Go to **Clusters** → **Connect** → **Connect your application**
2. Copy the connection string, it looks like:
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/scamshield?retryWrites=true&w=majority
```
3. Replace `<password>` with your actual password

---

## Step 3: Deploy Backend to Render (Free)

1. Go to [Render.com](https://render.com) and sign up with GitHub
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `scamshield-api` |
| **Region** | Oregon (US West) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |
| **Plan** | **Free** |

5. Add **Environment Variables** (scroll down):

| Key | Value |
|-----|-------|
| `MONGODB_URL` | Your MongoDB Atlas connection string |
| `SECRET_KEY` | Click "Generate" for a random value |
| `JWT_SECRET_KEY` | Click "Generate" for a random value |
| `ENVIRONMENT` | `production` |
| `CORS_ORIGINS` | `*` (update after frontend deploy) |
| `PYTHON_VERSION` | `3.11.0` |
| `GOOGLE_CLIENT_ID` | Your Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google OAuth client secret |
| `GITHUB_CLIENT_ID` | Your GitHub OAuth client ID |
| `GITHUB_CLIENT_SECRET` | Your GitHub OAuth client secret |

6. Click **Create Web Service**
7. Wait for deployment (~3-5 minutes)
8. Copy your backend URL: `https://scamshield-api.onrender.com`

### ⚠️ Free Tier Note:
- Free Render apps **sleep after 15 minutes of inactivity**
- First request after sleep takes ~30 seconds (cold start)
- This is normal for free tier!

---

## Step 4: Deploy Frontend to Netlify (Free)

1. Go to [Netlify](https://www.netlify.com) and sign up with GitHub
2. Click **Add new site** → **Import an existing project**
3. Connect your GitHub repository
4. Configure:

| Setting | Value |
|---------|-------|
| **Branch** | `main` |
| **Base directory** | (leave empty) |
| **Build command** | (leave empty) |
| **Publish directory** | `frontend/public` |

5. Click **Deploy site**
6. Wait for deployment (~1 minute)

### Configure API Proxy:

1. Go to **Site Settings** → **Build & deploy** → **Environment**
2. Or update `netlify.toml` in your repo:

Edit `netlify.toml` and replace `YOUR-RENDER-APP` with your actual Render app name:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://scamshield-api.onrender.com/api/:splat"
  status = 200
  force = true
```

3. Push the change to GitHub - Netlify will auto-redeploy

---

## Step 5: Update OAuth Redirect URIs

### Google OAuth:
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Edit your OAuth 2.0 Client
3. Add to **Authorized JavaScript origins**:
   - `https://your-site-name.netlify.app`
4. Add to **Authorized redirect URIs**:
   - `https://scamshield-api.onrender.com/api/v1/auth/google/callback`

### GitHub OAuth:
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Edit your OAuth App
3. Update **Homepage URL**: `https://your-site-name.netlify.app`
4. Update **Authorization callback URL**: `https://scamshield-api.onrender.com/api/v1/auth/github/callback`

---

## Step 6: Update CORS on Render

1. Go to your Render dashboard
2. Select your `scamshield-api` service
3. Go to **Environment** tab
4. Update `CORS_ORIGINS` to: `https://your-site-name.netlify.app`
5. Click **Save Changes** - service will redeploy

---

## ✅ Your Free Deployment is Complete!

Your app is now live at:
- **Frontend**: `https://your-site-name.netlify.app`
- **Backend API**: `https://scamshield-api.onrender.com`
- **API Docs**: `https://scamshield-api.onrender.com/docs`

---

## 💡 Free Tier Limitations

| Service | Limit | What happens |
|---------|-------|--------------|
| **Render** | 750 hours/month | Enough for 1 app running 24/7 |
| **Render** | Sleeps after 15 min | Cold start on first request |
| **MongoDB Atlas** | 512 MB storage | Plenty for demo/small apps |
| **Netlify** | 100 GB bandwidth | More than enough for most sites |

---

## 🔧 Troubleshooting

### Backend won't start:
- Check **Logs** tab in Render dashboard
- Verify MongoDB connection string is correct
- Make sure all environment variables are set

### CORS errors:
- Update `CORS_ORIGINS` in Render to include your Netlify domain
- Make sure to include `https://`

### OAuth not working:
- Update redirect URIs in Google/GitHub console
- Make sure client ID/secret are set in Render environment

### Slow first load:
- This is normal! Free tier apps sleep and take ~30s to wake up
- Upgrade to Render paid tier ($7/mo) for always-on

---

## 🎉 Congratulations!

Your ScamShield app is now live and free! Share the Netlify URL with others to use your app.
