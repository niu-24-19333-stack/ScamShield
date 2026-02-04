# 🔄 VERCEL DEPLOYMENT - CONFIGURATION UPDATE GUIDE

## ✅ **REQUIRED CHANGES FOR VERCEL DEPLOYMENT**

### **1️⃣ Update Backend Environment Variables**

After you get your Vercel deployment URL, update these:

```env
# In backend/.env
FRONTEND_URL=https://YOUR-VERCEL-APP.vercel.app

# OAuth Redirect URIs need updating too:
GOOGLE_REDIRECT_URI=https://scamshield-api-hocl.onrender.com/api/v1/auth/google/callback
GITHUB_REDIRECT_URI=https://scamshield-api-hocl.onrender.com/api/v1/auth/github/callback
```

### **2️⃣ Update OAuth Provider Settings**

**Google Cloud Console:**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Edit your OAuth 2.0 Client ID
3. Add to **Authorized redirect URIs**:
   - `https://YOUR-VERCEL-APP.vercel.app`
   - `https://scamshield-api-hocl.onrender.com/api/v1/auth/google/callback`

**GitHub OAuth Settings:**
1. Go to: https://github.com/settings/developers
2. Edit your OAuth App
3. Update **Authorization callback URL**:
   - `https://scamshield-api-hocl.onrender.com/api/v1/auth/github/callback`

### **3️⃣ Remove Netlify Configuration (Optional)**

Since you're no longer using Netlify:

```bash
# Remove netlify.toml (it's not needed for Vercel)
rm netlify.toml
```

### **4️⃣ Verify Vercel Configuration**

Make sure these files are properly configured:

**✅ vercel.json** (already created)
```json
{
  "outputDirectory": "public-deploy",
  "buildCommand": "echo 'No build needed'",
  "installCommand": "echo 'No dependencies'"
}
```

**✅ Frontend API Configuration** (already updated)
```javascript
// frontend/public/js/config.js
API_URL: 'https://scamshield-api-hocl.onrender.com'
```

### **5️⃣ Test After Deployment**

After updating configurations, test these features:
- ✅ **Homepage loads**
- ✅ **User registration works**
- ✅ **User login works**  
- ✅ **Admin login**: `raghavshivam4321@gmail.com` / `Thakur.4321`
- ✅ **Google OAuth login**
- ✅ **GitHub OAuth login**

## 🚀 **DEPLOYMENT STEPS**

1. **Get your Vercel URL** from Vercel dashboard
2. **Update FRONTEND_URL** in backend/.env
3. **Update OAuth redirect URIs** in Google & GitHub
4. **Redeploy backend** to Render with new environment variables
5. **Test all functionality**

## ⚡ **IMMEDIATE ACTION NEEDED:**

**Please provide your Vercel deployment URL so I can update the exact configuration!**

Example: `https://scamshield-abc123.vercel.app`

## 🔧 **Current Configuration Status:**

- ✅ **Backend CORS**: Configured for all origins
- ✅ **Vercel Config**: `vercel.json` created
- ✅ **Frontend API**: Points to correct backend
- ⏳ **Frontend URL**: Needs your Vercel URL
- ⏳ **OAuth Redirects**: Need updating with new URL