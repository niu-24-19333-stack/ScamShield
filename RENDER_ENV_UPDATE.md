# 🔧 Render.com Environment Update Guide

## ⚡ **CRITICAL: Update Backend Environment Variables**

Your Vercel URL: `https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app`

### **📝 Steps to Update Render.com:**

1. **Go to Render.com Dashboard**
   - Navigate to your `scamshield-api` service
   - Go to **Environment** tab

2. **Update FRONTEND_URL Variable:**
   ```
   Variable: FRONTEND_URL
   Value: https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app
   ```

3. **Save Changes**
   - Click "Save Changes"
   - Render will automatically redeploy with new settings

### **🔐 OAuth Redirect URLs to Update:**

**Google Cloud Console:**
- Go to: https://console.cloud.google.com/apis/credentials
- Find your OAuth 2.0 Client ID
- Add authorized redirect URI: 
  ```
  https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app/dashboard.html
  ```

**GitHub OAuth App:**
- Go to: https://github.com/settings/developers
- Find your OAuth App
- Update Authorization callback URL:
  ```
  https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app/dashboard.html
  ```

### **🧪 Test After Updates:**

1. **Visit your Vercel app:** https://scam-shield-1yzg-42nohqy3p-morbius-projects-43b3a6c9.vercel.app
2. **Test login flows:** Google OAuth, GitHub OAuth, Email/Password
3. **Test admin access:** raghavshivam4321@gmail.com / Admin123!

### **✅ Expected Results:**
- ✅ Frontend loads without CORS errors
- ✅ API calls reach backend successfully  
- ✅ OAuth redirects work properly
- ✅ Admin dashboard accessible

---
**⏰ ETA: ~5 minutes for Render redeployment after environment update**