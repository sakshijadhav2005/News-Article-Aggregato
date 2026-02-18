# 📸 Render Deployment - Visual Step-by-Step Guide

## 🎯 Deploy Both Backend & Frontend on Render.com

---

## Before You Start

✅ Make sure your code is pushed to GitHub:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

---

## Step 1: Go to Render.com

1. Open your browser
2. Go to: **https://render.com**
3. You'll see the Render homepage

---

## Step 2: Sign Up with GitHub

1. Click **"Get Started"** or **"Sign Up"** button
2. Choose **"Sign up with GitHub"**
3. Enter your GitHub credentials
4. Click **"Authorize Render"**
5. You'll be redirected to Render dashboard

---

## Step 3: Create New Blueprint

1. You'll see the Render Dashboard
2. Look for the **"New +"** button (top right corner)
3. Click **"New +"**
4. A dropdown menu appears
5. Select **"Blueprint"**

---

## Step 4: Connect Repository

1. You'll see "Create a new Blueprint Instance" page
2. Click **"Connect a repository"** button
3. You'll see a list of your GitHub repositories
4. Find **"news-article-aggregator"** (or your repo name)
5. Click **"Connect"** next to it

---

## Step 5: Render Detects Configuration

1. Render automatically reads your `render.yaml` file
2. You'll see a page showing:
   ```
   Blueprint: news-article-aggregator
   
   Services to be created:
   ✓ news-aggregator-api (Web Service)
   ✓ news-aggregator-frontend (Web Service)
   ```
3. Both services are listed with their configurations

---

## Step 6: Review and Apply

1. Review the services:
   - **news-aggregator-api**: Python, Free plan
   - **news-aggregator-frontend**: Node, Free plan
2. Click the blue **"Apply"** button at the bottom
3. Render starts creating both services

---

## Step 7: Watch Deployment Progress

### Backend (news-aggregator-api):

You'll see logs like:
```
==> Cloning from https://github.com/YOUR_USERNAME/news-article-aggregator...
==> Checking out commit abc123...
==> Running build command: cd backend && pip install -r requirements-real.txt
==> Installing dependencies...
==> Build successful!
==> Starting service...
==> Your service is live 🎉
```

**Status changes:**
- 🟡 Yellow "Building" → 🟢 Green "Live"

### Frontend (news-aggregator-frontend):

You'll see logs like:
```
==> Cloning from https://github.com/YOUR_USERNAME/news-article-aggregator...
==> Running build command: cd frontend && npm install && npm run build
==> Installing dependencies...
==> Building application...
==> Build successful!
==> Starting service...
==> Your service is live 🎉
```

**Status changes:**
- 🟡 Yellow "Building" → 🟢 Green "Live"

**⏱️ Total time: 10-15 minutes**

---

## Step 8: Get Your URLs

### After deployment completes:

1. Go to your Render Dashboard
2. You'll see both services listed:

**Backend:**
```
news-aggregator-api
Status: 🟢 Live
URL: https://news-aggregator-api.onrender.com
```

**Frontend:**
```
news-aggregator-frontend
Status: 🟢 Live
URL: https://news-aggregator-frontend.onrender.com
```

3. **Copy both URLs** - you'll need them!

---

## Step 9: Configure Frontend Environment Variable

**IMPORTANT:** Tell the frontend where the backend is.

1. Click on **"news-aggregator-frontend"** service
2. Click **"Environment"** tab (left sidebar)
3. You'll see "Environment Variables" section
4. Click **"Add Environment Variable"** button
5. Fill in:
   ```
   Key: VITE_API_URL
   Value: https://news-aggregator-api.onrender.com/api/v1
   ```
6. Click **"Save Changes"**
7. Frontend will automatically redeploy (takes 2-3 minutes)

---

## Step 10: Test Your Live App!

### Test Backend:

1. Open: `https://news-aggregator-api.onrender.com/docs`
2. You should see the API documentation (Swagger UI)
3. Try the `/api/v1/health` endpoint
4. Should return: `{"success": true, "data": {"status": "healthy"}}`

### Test Frontend:

1. Open: `https://news-aggregator-frontend.onrender.com`
2. You should see your beautiful homepage
3. Click **"Fetch Articles"** button
4. Wait 10-20 seconds (backend is waking up)
5. You should see real news articles appear!
6. Try browsing, filtering, and viewing clusters

---

## ✅ Success Checklist

- [ ] Backend shows 🟢 "Live" status
- [ ] Frontend shows 🟢 "Live" status
- [ ] Backend URL opens API docs
- [ ] Frontend URL opens homepage
- [ ] Can fetch articles
- [ ] Articles display correctly
- [ ] Can filter by source/topic
- [ ] Can view clusters
- [ ] "View Original" opens real news sites

---

## 🎨 What You'll See in Render Dashboard

### Dashboard View:
```
┌─────────────────────────────────────────┐
│  news-aggregator-api                    │
│  🟢 Live                                 │
│  https://news-aggregator-api.onrender.com
│  Last deployed: 2 minutes ago           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  news-aggregator-frontend               │
│  🟢 Live                                 │
│  https://news-aggregator-frontend.onrender.com
│  Last deployed: 1 minute ago            │
└─────────────────────────────────────────┘
```

### Service Details (click on a service):
```
Tabs:
- Events (deployment history)
- Logs (real-time logs)
- Metrics (CPU, memory, requests)
- Environment (environment variables)
- Settings (service configuration)
```

---

## 🔄 Auto-Deploy Setup

**Already configured!** Every time you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Add new feature"
git push origin main
```

**Render automatically:**
1. Detects the push
2. Rebuilds affected services
3. Deploys new version
4. No manual action needed! 🎉

---

## 📱 Share Your App

**For Hackathon Submission:**

```
Live Demo: https://news-aggregator-frontend.onrender.com
API Docs: https://news-aggregator-api.onrender.com/docs
GitHub: https://github.com/YOUR_USERNAME/news-article-aggregator
```

**For Social Media:**

```
🚀 Just deployed my AI-Powered News Aggregator!

✅ Fetches real news from BBC, CNN, Guardian
✅ AI summarization & clustering
✅ Beautiful React UI
✅ FastAPI backend

Try it: https://news-aggregator-frontend.onrender.com

#hackathon #webdev #AI
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend shows "Application Error"

**Cause:** Free tier services sleep after 15 minutes

**Solution:** 
- Wait 30 seconds, refresh page
- Backend will wake up automatically
- First request after sleep is slow

### Issue 2: Frontend can't connect to backend

**Cause:** Missing or wrong `VITE_API_URL`

**Solution:**
1. Go to frontend service
2. Environment tab
3. Add/update `VITE_API_URL`
4. Value: `https://news-aggregator-api.onrender.com/api/v1`
5. Save and wait for redeploy

### Issue 3: Build fails

**Cause:** Missing dependencies or wrong paths

**Solution:**
1. Check logs for specific error
2. Make sure `render.yaml` is in root directory
3. Make sure `requirements-real.txt` is in `backend/` folder
4. Make sure `package.json` is in `frontend/` folder

### Issue 4: "No articles found"

**Cause:** Haven't fetched articles yet

**Solution:**
1. Click "Fetch Articles" button
2. Wait 10-20 seconds
3. Articles will appear

---

## 💡 Pro Tips

### Tip 1: Keep Backend Awake

Use **UptimeRobot** (free):
1. Sign up at https://uptimerobot.com
2. Add monitor: `https://news-aggregator-api.onrender.com/api/v1/health`
3. Check interval: 5 minutes
4. Backend stays awake!

### Tip 2: View Real-Time Logs

```
Dashboard → Service → Logs tab
```
See every request, error, and event in real-time

### Tip 3: Manual Redeploy

If something goes wrong:
```
Dashboard → Service → Manual Deploy → Deploy latest commit
```

### Tip 4: Clear Build Cache

If build is stuck:
```
Dashboard → Service → Manual Deploy → Clear build cache & deploy
```

---

## 🎉 Congratulations!

Your News Aggregator is now:
- 🌍 **Live** on the internet
- 🔒 **Secured** with HTTPS
- 📱 **Accessible** from any device
- 🚀 **Auto-deploys** on git push
- 💯 **100% FREE** to host

**Both backend and frontend deployed from ONE repository!**

---

## 📞 Need More Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Render Status**: https://status.render.com

---

**Now go show off your live app! 🏆**
