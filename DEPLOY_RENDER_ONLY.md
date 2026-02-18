# 🚀 Deploy BOTH Backend & Frontend on Render.com (FREE)

## Why Render for Both?
- ✅ 100% FREE
- ✅ Deploy both services from ONE repository
- ✅ Auto-deploy on git push
- ✅ HTTPS included
- ✅ Easy to manage

---

## 📋 Prerequisites

1. **Push your code to GitHub** (if not already done):
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Make sure these files exist** (they should already):
   - `render.yaml` (in root directory)
   - `backend/requirements-real.txt`
   - `frontend/package.json`

---

## 🎯 Step-by-Step Deployment

### Step 1: Sign Up on Render

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with your **GitHub account**
4. Authorize Render to access your repositories

### Step 2: Deploy Using Blueprint

1. After logging in, click **"New +"** button (top right)
2. Select **"Blueprint"**
3. Click **"Connect a repository"**
4. Find and select your `news-article-aggregator` repository
5. Click **"Connect"**

### Step 3: Render Detects Configuration

Render will automatically detect `render.yaml` and show:
- ✅ **news-aggregator-api** (Backend)
- ✅ **news-aggregator-frontend** (Frontend)

### Step 4: Apply Blueprint

1. Review the services (should show 2 services)
2. Click **"Apply"** button
3. Render will start deploying BOTH services

### Step 5: Wait for Deployment (10-15 minutes)

**Backend deployment:**
- Installing Python packages
- Building application
- Starting server
- Status will change to "Live" (green)

**Frontend deployment:**
- Installing npm packages
- Building React app
- Starting preview server
- Status will change to "Live" (green)

### Step 6: Get Your URLs

After deployment completes, you'll have:

**Backend API:**
```
https://news-aggregator-api.onrender.com
```

**Frontend App:**
```
https://news-aggregator-frontend.onrender.com
```

### Step 7: Update Frontend API URL

**IMPORTANT:** The frontend needs to know where the backend is.

1. In Render dashboard, click on **"news-aggregator-frontend"**
2. Go to **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   ```
   Key: VITE_API_URL
   Value: https://news-aggregator-api.onrender.com/api/v1
   ```
5. Click **"Save Changes"**
6. Frontend will automatically redeploy

### Step 8: Test Your App

1. Open your frontend URL: `https://news-aggregator-frontend.onrender.com`
2. Click **"Fetch Articles"** button
3. Wait 10-20 seconds (first request wakes up the backend)
4. You should see real news articles!

---

## ✅ Verification Checklist

- [ ] Backend is "Live" (green status)
- [ ] Frontend is "Live" (green status)
- [ ] Frontend opens in browser
- [ ] Can click "Fetch Articles"
- [ ] Articles appear after fetching
- [ ] Can browse articles
- [ ] Can view clusters
- [ ] "View Original" opens real news sites

---

## 🔧 Troubleshooting

### Backend shows "Deploy failed"

**Check logs:**
1. Click on "news-aggregator-api"
2. Go to "Logs" tab
3. Look for error messages

**Common issues:**
- Missing `requirements-real.txt` → Make sure it's in `backend/` folder
- Python version error → Check `render.yaml` has `PYTHON_VERSION: 3.11.0`

**Fix:**
```bash
# Make sure file exists
ls backend/requirements-real.txt

# If missing, create it
cd backend
pip freeze > requirements-real.txt

# Commit and push
git add .
git commit -m "Add requirements file"
git push origin main
```

### Frontend shows "Deploy failed"

**Check logs:**
1. Click on "news-aggregator-frontend"
2. Go to "Logs" tab
3. Look for error messages

**Common issues:**
- Missing `package.json` → Make sure it's in `frontend/` folder
- Build errors → Check if `npm run build` works locally

**Fix:**
```bash
# Test build locally
cd frontend
npm install
npm run build

# If it works, push to GitHub
git add .
git commit -m "Fix frontend build"
git push origin main
```

### Frontend loads but shows "No articles"

**This is normal!** The backend is sleeping.

**Solution:**
1. Wait 30 seconds for backend to wake up
2. Click "Fetch Articles" again
3. Backend will wake up and fetch articles

### Frontend can't connect to backend

**Check environment variable:**
1. Go to frontend service in Render
2. Click "Environment" tab
3. Make sure `VITE_API_URL` is set correctly:
   ```
   https://news-aggregator-api.onrender.com/api/v1
   ```
4. Save and wait for redeploy

### "Application Error" on backend

**Render free tier sleeps after 15 minutes of inactivity.**

**This is normal!** The backend will wake up when you visit it.

**To keep it awake (optional):**
1. Sign up at https://uptimerobot.com (free)
2. Add your backend URL
3. Set ping interval to 5 minutes
4. Backend stays awake!

---

## 🎨 Customize Your URLs (Optional)

### Change Service Names

1. Go to service settings
2. Click "Settings" tab
3. Change "Name" field
4. Your URL will update to: `https://your-new-name.onrender.com`

### Add Custom Domain (Optional)

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Render, go to service settings
3. Click "Custom Domains"
4. Add your domain
5. Update DNS records as instructed
6. Your app at: `www.yourdomain.com`

---

## 🔄 Auto-Deploy on Git Push

**Already set up!** Every time you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render automatically:
1. Detects the push
2. Rebuilds both services
3. Deploys new version
4. Your app updates! 🎉

---

## 📊 Monitor Your Services

### View Logs

**Backend logs:**
1. Dashboard → news-aggregator-api
2. Click "Logs" tab
3. See real-time logs

**Frontend logs:**
1. Dashboard → news-aggregator-frontend
2. Click "Logs" tab
3. See build and runtime logs

### Check Status

**Dashboard shows:**
- 🟢 Green = Live and running
- 🟡 Yellow = Deploying
- 🔴 Red = Failed or stopped

### View Metrics

1. Click on service
2. Go to "Metrics" tab
3. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## 💰 Cost Breakdown

**Render Free Tier:**
- ✅ 750 hours/month per service
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ✅ Custom domains
- ⚠️ Services sleep after 15 min inactivity
- ⚠️ Takes 30 seconds to wake up

**Upgrade to Paid ($7/month per service):**
- ✅ No sleeping
- ✅ Faster builds
- ✅ More resources
- ✅ Better performance

---

## 🎯 For Hackathon Demo

### Share These Links:

**Live App:**
```
https://news-aggregator-frontend.onrender.com
```

**API Documentation:**
```
https://news-aggregator-api.onrender.com/docs
```

**GitHub Repository:**
```
https://github.com/YOUR_USERNAME/news-article-aggregator
```

### Demo Tips:

1. **Wake up services before demo:**
   - Visit both URLs 5 minutes before presenting
   - Click "Fetch Articles" to warm up backend
   
2. **Explain the tech:**
   - "Deployed on Render.com"
   - "Auto-deploys from GitHub"
   - "Fetches real news from BBC, CNN, etc."
   - "Uses AI for summarization and clustering"

3. **Show the features:**
   - Fetch articles
   - Browse and filter
   - View clusters
   - Click "View Original" to show real news

---

## 🎉 Success!

Your News Aggregator is now:
- 🌍 Live on the internet
- 🔒 Secured with HTTPS
- 📱 Accessible from anywhere
- 🚀 Auto-deploys on git push
- 💯 100% FREE

**Both services deployed from ONE repository!**

---

## 📞 Need Help?

**Render Support:**
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**Common Commands:**

```bash
# View your services
# Go to: https://dashboard.render.com

# Trigger manual deploy
# Dashboard → Service → Manual Deploy → Deploy latest commit

# View logs
# Dashboard → Service → Logs

# Restart service
# Dashboard → Service → Manual Deploy → Clear build cache & deploy
```

---

**Your app is live! Now go impress those judges! 🏆**
