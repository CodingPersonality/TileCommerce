# Render + Neon Deployment Guide for TileCommerce

## Why Render + Neon?

✅ **Completely FREE** (no credit card needed as of 2026)
✅ **Permanent Database** (Neon data never deletes after 30 days)
✅ **Professional Setup** (PostgreSQL, industry standard)
✅ **Easy Deployment** (automatic from GitHub)
✅ **Your data is yours** (separate from hosting platform)

---

## Phase 1: Create Your Neon Database

### Step 1: Sign Up at Neon
1. Go to https://neon.tech
2. Click **"Sign Up"** (use GitHub or email)
3. Verify your email

### Step 2: Create a New Project
1. Click **"New Project"**
2. **Project Name**: `tilecommerce`
3. **Region**: Select closest to you (e.g., US East)
4. Click **"Create project"**

### Step 3: Get Your Database URL
1. Once created, you'll see your dashboard
2. Look for **"Connection string"** section
3. Copy the **Postgres** connection string
4. It looks like: `postgresql://user:password@host/database`
5. **Keep this safe!** You'll need it for Render

---

## Phase 2: Deploy to Render

### Step 1: Sign Up at Render
1. Go to https://render.com
2. Click **"Sign Up"**
3. Use your **GitHub account** (recommended)
4. Authorize Render to access your repos

### Step 2: Create Web Service
1. Click **"+ New"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Select **CodingPersonality/TileCommerce**
4. Click **"Connect"**

### Step 3: Configure Web Service
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `tilecommerce` |
| **Environment** | `Python 3` |
| **Region** | Same as Neon (e.g., Oregon) |
| **Branch** | `main` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn TileCommerce.wsgi:application` |
| **Plan** | `Free` |

### Step 4: Add Environment Variables

Click **"Advanced"** section, then click **"Add Environment Variable"**

Add these 3 variables:

1. **DATABASE_URL**
   - **Key**: `DATABASE_URL`
   - **Value**: (Paste your Neon connection string from Phase 1)
   - Example: `postgresql://user:password@ep-cool-darkness-12345.us-east-2.aws.neon.tech/neondb`

2. **SECRET_KEY**
   - **Key**: `SECRET_KEY`
   - **Value**: Run this locally and copy the result:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **PYTHON_VERSION**
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.10.13`

4. **DEBUG**
   - **Key**: `DEBUG`
   - **Value**: `False`

### Step 5: Deploy!
1. Click the blue **"Deploy"** button
2. Watch the build logs (takes 3-5 minutes)
3. You'll see: ✅ **"Your service is live"**
4. Your site is at: `https://tilecommerce.onrender.com`

---

## What Happens During Deployment

1. **Render pulls your code** from GitHub
2. **Runs build.sh** which:
   - Installs all Python packages
   - Collects static files (CSS, images, JS)
   - Migrates database (creates tables in Neon)
3. **Starts your app** with Gunicorn
4. **Your site is live!** 🎉

---

## Your Site is Now Live!

**Visit**: `https://tilecommerce.onrender.com`

Your data is safely stored in **Neon** (separate database platform).

If you ever need to move hosting, your data is yours - you can export it anytime!

---

## After Deployment: Making Updates

**Every time you change your code:**

1. Make changes locally
2. Commit and push to GitHub:
```bash
git add -A
git commit -m "Your message"
git push origin main
```

3. **Render automatically redeploys** within 2 minutes! ✨

No manual steps needed - it's automatic!

---

## Need an Admin Account?

If you want to access Django admin panel:

1. Go to your **Web Service** on Render dashboard
2. Click the **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```

4. Follow the prompts
5. Access admin at: `https://tilecommerce.onrender.com/admin`

---

## Important Files Explained

| File | Purpose |
|------|---------|
| `render.yaml` | Tells Render how to deploy your app |
| `build.sh` | Build script that runs on Render |
| `requirements.txt` | Python packages Render needs to install |
| `.env.example` | Template for environment variables |

---

## Troubleshooting

### "Deployment Failed"
1. Check the **Build Logs** tab
2. Look for error messages
3. Common issues:
   - Typo in DATABASE_URL
   - Missing required fields
   - Old code from GitHub (try force push)

### "Database Connection Error"
1. Verify DATABASE_URL is correct
2. Make sure Neon project is still active
3. Try redeploying

### "Static Files Not Loading"
1. This shouldn't happen - WhiteNoise handles it
2. If it does, check the logs
3. Try: `git add -A && git push origin main` (auto-redeploy)

### Website is Slow on First Load
- Normal! Free tier Neon database goes to sleep after 15 min of no activity
- First request might take 5-10 seconds to wake up
- Subsequent requests are instant

---

## Upgrade Options (Not Required)

### Free Tier Limitations
- Neon free: 10 connections, 3 GB storage (plenty for most apps!)
- Render free: Limited compute power
- Both restart/sleep after inactivity

### If You Want Production Quality
- **Render Web Service**: $7/month (for always-on server)
- **Neon PostgreSQL**: $15-50/month (for always-on database)

**But the free tier works great for testing!**

---

## Support & Documentation

- **Neon Docs**: https://neon.tech/docs
- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com/

---

## Summary

| Platform | Cost | What it Does |
|----------|------|-------------|
| **Render** | Free | Hosts your Django code |
| **Neon** | Free | Stores your database |
| **GitHub** | Free | Version control |
| **Your App** | FREE! | Live on internet 🚀 |

**Total setup time: ~15 minutes**
**Total cost: $0**
**Your data: Yours forever**

---

**🎉 Congratulations! Your site is live!**

Now go build something amazing! 💪
