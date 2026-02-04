# ScamShield Frontend Deployment Guide

## 🚀 Quick Deploy Options (All Free)

### Option 1: GitHub Pages (EASIEST - Just set up!)
1. ✅ **Already configured** - deployment workflow added
2. Go to: https://github.com/niu-24-19333-stack/ScamShield/settings/pages
3. Set **Source** to "GitHub Actions"
4. Your site will be live at: **https://niu-24-19333-stack.github.io/ScamShield/**

### Option 2: Vercel (FASTEST)
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "New Project" → Select "ScamShield" repo
4. Set **Root Directory**: `frontend/public`
5. Click Deploy

### Option 3: Surge.sh (SIMPLE)
```bash
# Install surge globally
npm install -g surge

# Navigate to frontend folder
cd frontend/public

# Deploy (will ask for domain name)
surge
```

### Option 4: Firebase Hosting
1. Install Firebase CLI: `npm install -g firebase-tools`
2. Run: `firebase login`
3. Run: `firebase init hosting`
4. Set public directory: `frontend/public`
5. Run: `firebase deploy`

### Option 5: Render Static Sites
1. Go to https://render.com
2. Connect GitHub → Select ScamShield
3. Choose "Static Site"
4. Set **Publish Directory**: `frontend/public`
5. Deploy

## 🔧 After Deployment:
1. Update your backend `.env` file:
   ```env
   FRONTEND_URL=https://your-new-domain.com
   ```
2. Test the deployment
3. Update OAuth redirect URIs if needed

## 🎯 Recommended: Use GitHub Pages
- ✅ Already set up for you
- ✅ Free forever
- ✅ Custom domain support
- ✅ Automatic deployments