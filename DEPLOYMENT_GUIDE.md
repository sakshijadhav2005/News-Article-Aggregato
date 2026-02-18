# 🚀 Deployment Guide - Host Your News Aggregator

This guide covers multiple hosting options from free to production-grade.

---

## 📋 Table of Contents

1. [Quick Deploy (Free) - Render + Vercel](#option-1-free-hosting---render--vercel)
2. [Railway (Easy, Paid)](#option-2-railway-easy-all-in-one)
3. [Heroku (Traditional)](#option-3-heroku-traditional)
4. [AWS (Production)](#option-4-aws-production-grade)
5. [Docker + VPS](#option-5-docker--vps-digital-ocean-linode)

---

## Option 1: Free Hosting - Render + Vercel

**Best for:** Hackathon demos, portfolios
**Cost:** FREE
**Time:** 15 minutes

### Backend on Render (Free)

**1. Create `render.yaml` in project root:**

```yaml
services:
  - type: web
    name: news-aggregator-api
    env: python
    buildCommand: "cd backend && pip install -r requirements-real.txt"
    startCommand: "cd backend && uvicorn src.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 8000
```

**2. Deploy to Render:**
- Go to https://render.com
- Sign up with GitHub
- Click "New +" → "Blueprint"
- Connect your GitHub repository
- Render will auto-detect `render.yaml`
- Click "Apply"
- Wait 5-10 minutes for deployment

**3. Get your backend URL:**
```
https://news-aggregator-api.onrender.com
```

### Frontend on Vercel (Free)

**1. Update frontend API URL:**

Create `frontend/.env.production`:
```env
VITE_API_URL=https://news-aggregator-api.onrender.com/api/v1
```

**2. Create `vercel.json` in frontend folder:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**3. Deploy to Vercel:**
- Go to https://vercel.com
- Sign up with GitHub
- Click "Add New" → "Project"
- Import your repository
- Set root directory to `frontend`
- Click "Deploy"

**4. Your app is live!**
```
https://your-app.vercel.app
```

---

## Option 2: Railway (Easy, All-in-One)

**Best for:** Quick deployment, no config
**Cost:** $5/month (free trial available)
**Time:** 10 minutes

### Deploy Both Backend & Frontend

**1. Create `railway.json`:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn src.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**2. Deploy:**
- Go to https://railway.app
- Sign up with GitHub
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository
- Railway auto-detects and deploys
- Add environment variables if needed

**3. Deploy Frontend:**
- Click "New" → "GitHub Repo" again
- Select same repo
- Set root directory to `frontend`
- Add environment variable:
  ```
  VITE_API_URL=https://your-backend.railway.app/api/v1
  ```

**Done!** Both services are live.

---

## Option 3: Heroku (Traditional)

**Best for:** Established platform, easy scaling
**Cost:** $7/month per dyno
**Time:** 20 minutes

### Backend Deployment

**1. Create `Procfile` in backend folder:**
```
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**2. Create `runtime.txt` in backend folder:**
```
python-3.11.0
```

**3. Deploy:**
```bash
# Install Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create news-aggregator-api

# Deploy backend
cd backend
git init
git add .
git commit -m "Deploy backend"
heroku git:remote -a news-aggregator-api
git push heroku main

# Get URL
heroku open
```

### Frontend Deployment

**1. Update API URL in `frontend/.env.production`:**
```env
VITE_API_URL=https://news-aggregator-api.herokuapp.com/api/v1
```

**2. Build and deploy:**
```bash
cd frontend
npm run build

# Deploy to Vercel or Netlify (easier than Heroku for static sites)
```

---

## Option 4: AWS (Production Grade)

**Best for:** Production apps, full control
**Cost:** ~$20-50/month
**Time:** 1-2 hours

### Architecture
- **Backend**: AWS Elastic Beanstalk or ECS
- **Frontend**: S3 + CloudFront
- **Database**: RDS (optional)
- **Cache**: ElastiCache (optional)

### Backend on Elastic Beanstalk

**1. Install EB CLI:**
```bash
pip install awsebcli
```

**2. Initialize:**
```bash
cd backend
eb init -p python-3.11 news-aggregator-api
```

**3. Create environment:**
```bash
eb create news-aggregator-env
```

**4. Deploy:**
```bash
eb deploy
```

**5. Get URL:**
```bash
eb open
```

### Frontend on S3 + CloudFront

**1. Build frontend:**
```bash
cd frontend
npm run build
```

**2. Create S3 bucket:**
```bash
aws s3 mb s3://news-aggregator-frontend
```

**3. Upload:**
```bash
aws s3 sync dist/ s3://news-aggregator-frontend --acl public-read
```

**4. Enable static website hosting:**
- Go to S3 console
- Select bucket
- Properties → Static website hosting → Enable
- Index document: `index.html`

**5. Create CloudFront distribution:**
- Go to CloudFront console
- Create distribution
- Origin: Your S3 bucket
- Default root object: `index.html`

---

## Option 5: Docker + VPS (Digital Ocean, Linode)

**Best for:** Full control, cost-effective
**Cost:** $5-10/month
**Time:** 30 minutes

### Setup VPS

**1. Create droplet:**
- Go to https://digitalocean.com or https://linode.com
- Create Ubuntu 22.04 droplet ($5/month)
- Add SSH key

**2. Connect:**
```bash
ssh root@your-server-ip
```

**3. Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

**4. Install Docker Compose:**
```bash
apt install docker-compose
```

### Deploy with Docker

**1. Update `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://your-server-ip:8000/api/v1
    restart: always
```

**2. Create `backend/Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-real.txt .
RUN pip install --no-cache-dir -r requirements-real.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**3. Create `frontend/Dockerfile`:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**4. Create `frontend/nginx.conf`:**
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**5. Deploy:**
```bash
# On your VPS
git clone https://github.com/YOUR_USERNAME/news-article-aggregator.git
cd news-article-aggregator
docker-compose up -d
```

**6. Access your app:**
```
http://your-server-ip
```

### Setup Domain (Optional)

**1. Point domain to server IP:**
- Add A record: `@` → `your-server-ip`
- Add A record: `www` → `your-server-ip`

**2. Install SSL with Let's Encrypt:**
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 🔒 Security Checklist

Before going live:

- [ ] Change all default passwords
- [ ] Set up environment variables (don't commit `.env`)
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS properly
- [ ] Add rate limiting
- [ ] Enable firewall (UFW on Ubuntu)
- [ ] Regular backups
- [ ] Monitor logs

---

## 📊 Monitoring & Maintenance

### Free Monitoring Tools
- **Uptime**: UptimeRobot (https://uptimerobot.com)
- **Errors**: Sentry (https://sentry.io)
- **Analytics**: Google Analytics
- **Logs**: Papertrail (https://papertrailapp.com)

### Maintenance Tasks
- Update dependencies monthly
- Monitor disk space
- Check error logs weekly
- Backup data regularly

---

## 🎯 Recommended for Hackathon

**Best Option:** Render (Backend) + Vercel (Frontend)
- ✅ FREE
- ✅ Fast deployment (15 min)
- ✅ Auto-deploy on git push
- ✅ SSL included
- ✅ Good performance
- ✅ Easy to demo

**Commands:**
```bash
# 1. Push to GitHub
git push origin main

# 2. Connect Render to GitHub repo
# 3. Connect Vercel to GitHub repo
# 4. Done! Your app is live
```

---

## 🆘 Troubleshooting

### Backend won't start
- Check Python version (3.11+)
- Verify all dependencies installed
- Check environment variables
- Review logs

### Frontend can't connect to backend
- Verify API URL in `.env.production`
- Check CORS settings in backend
- Ensure backend is running
- Check network/firewall

### Slow performance
- Enable caching
- Use CDN for frontend
- Optimize images
- Add database indexes

---

## 📞 Need Help?

- Check logs first
- Review error messages
- Search Stack Overflow
- Check platform documentation

---

**Your app is ready to deploy! Choose the option that fits your needs and budget.** 🚀
