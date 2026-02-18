# 🚀 Deploy Your App NOW - 15 Minutes

## Fastest Way: Render + Vercel (100% FREE)

### Step 1: Deploy Backend (5 minutes)

1. **Go to Render**: https://render.com
2. **Sign up** with your GitHub account
3. Click **"New +"** → **"Blueprint"**
4. **Connect your repository**
5. Render will find `render.yaml` automatically
6. Click **"Apply"**
7. Wait 5-10 minutes for build

**Your backend will be live at:**
```
https://news-aggregator-api.onrender.com
```

### Step 2: Deploy Frontend (5 minutes)

1. **Update API URL** in `frontend/.env.production`:
   ```env
   VITE_API_URL=https://news-aggregator-api.onrender.com/api/v1
   ```

2. **Go to Vercel**: https://vercel.com
3. **Sign up** with your GitHub account
4. Click **"Add New"** → **"Project"**
5. **Import your repository**
6. Set **Root Directory** to `frontend`
7. Click **"Deploy"**
8. Wait 2-3 minutes

**Your frontend will be live at:**
```
https://your-app-name.vercel.app
```

### Step 3: Test Your Live App

1. Open your Vercel URL
2. Click "Fetch Articles"
3. Wait 10-20 seconds (first fetch is slow)
4. Browse articles with REAL news!

---

## ✅ That's It!

Your app is now:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Free to host
- ✅ Auto-deploys on git push
- ✅ Has SSL/HTTPS
- ✅ Ready for hackathon demo

---

## 🔗 Share Your App

**Backend API:**
```
https://news-aggregator-api.onrender.com/docs
```

**Frontend App:**
```
https://your-app-name.vercel.app
```

**GitHub Repo:**
```
https://github.com/YOUR_USERNAME/news-article-aggregator
```

---

## 🐛 Troubleshooting

### Backend build fails
- Check `render.yaml` is in root directory
- Verify `requirements-real.txt` exists in backend folder
- Check Render logs for specific error

### Frontend can't connect to backend
1. Make sure backend is deployed first
2. Update `frontend/.env.production` with correct backend URL
3. Redeploy frontend on Vercel

### "Application error" on Render
- Wait 10 minutes for first deployment
- Check Render logs
- Render free tier sleeps after 15 min of inactivity (wakes up on first request)

---

## 💡 Pro Tips

### Keep Backend Awake
Render free tier sleeps after 15 minutes. To keep it awake:

1. Use **UptimeRobot** (free): https://uptimerobot.com
2. Add your backend URL
3. Ping every 5 minutes
4. Backend stays awake!

### Custom Domain (Optional)
1. Buy domain from Namecheap/GoDaddy
2. In Vercel: Settings → Domains → Add
3. Follow DNS instructions
4. Your app at: `www.yourcustomdomain.com`

### Auto-Deploy on Push
Both Render and Vercel auto-deploy when you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Automatically deploys! 🎉
```

---

## 📊 Monitor Your App

### Check if it's up:
- **Backend**: https://news-aggregator-api.onrender.com/api/v1/health
- **Frontend**: https://your-app-name.vercel.app

### View logs:
- **Render**: Dashboard → Your service → Logs
- **Vercel**: Dashboard → Your project → Deployments → View logs

---

## 🎯 For Hackathon Judges

Share these links:
1. **Live Demo**: https://your-app-name.vercel.app
2. **API Docs**: https://news-aggregator-api.onrender.com/docs
3. **GitHub**: https://github.com/YOUR_USERNAME/news-article-aggregator
4. **Video Demo**: (Record a 2-min walkthrough)

---

## 🎉 Congratulations!

Your News Aggregator is now:
- 🌍 Live on the internet
- 🔒 Secured with HTTPS
- 📱 Accessible from any device
- 🚀 Ready to impress judges
- 💯 100% FREE to host

**Now go win that hackathon!** 🏆
