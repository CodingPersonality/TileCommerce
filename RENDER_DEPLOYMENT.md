# Render Deployment Guide for TileCommerce

## Overview
This guide will deploy your TileCommerce Django app to **Render** with a free PostgreSQL database.

**What you get:**
- ✅ Free web service
- ✅ Free PostgreSQL database (forever)
- ✅ Automatic deployments from GitHub
- ✅ Free SSL certificate (HTTPS)
- ✅ Easy to use

---

## Step 1: Create a Render Account

1. Go to https://render.com
2. Click **"Sign Up"**
3. Use your GitHub account to sign up (recommended)
4. Verify your email

---

## Step 2: Connect Your GitHub Repository

1. Log in to Render Dashboard
2. Click **"+ New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Select **CodingPersonality/TileCommerce**
5. Click **"Connect"**

---

## Step 3: Configure Your Web Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `tilecommerce` |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn TileCommerce.wsgi:application` |
| **Plan** | `Free` |

---

## Step 4: Add Environment Variables

1. Scroll down to **"Environment"** section
2. Click **"Add Environment Variable"**
3. Add these variables:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | (generate below) |
| `ALLOWED_HOSTS` | `tilecommerce.onrender.com` |
| `PYTHON_VERSION` | `3.10.13` |

### Generate a Secret Key

Run this command locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as the `SECRET_KEY` value.

---

## Step 5: Create PostgreSQL Database

1. In Render Dashboard, click **"+ New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name**: `tilecommerce-db`
   - **Database**: `tilecommerce`
   - **User**: `tilecommerce`
   - **Region**: Same as your web service
   - **Plan**: `Free`

3. Click **"Create Database"**
4. Wait for it to be created (~2 minutes)
5. Copy the **Internal Database URL**

---

## Step 6: Connect Database to Web Service

1. Go back to your **Web Service** (tilecommerce)
2. Click **"Environment"** tab
3. Add new environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from Step 5

---

## Step 7: Deploy Your App

1. Click the **"Deploy"** button
2. Watch the build logs (it takes 3-5 minutes)
3. You should see: ✅ **"Your service is live"**
4. Your app is now at: `https://tilecommerce.onrender.com`

---

## Step 8: Create Admin Account (Optional)

If you need an admin account, you can connect via SSH:

1. In your Web Service, click the **"Shell"** tab
2. Run:
```bash
python manage.py createsuperuser
```

3. Follow the prompts to create an admin user
4. Access admin at: `https://tilecommerce.onrender.com/admin`

---

## Step 9: Verify Deployment

1. Visit: `https://tilecommerce.onrender.com`
2. Your website should be live!
3. Check the logs if you encounter errors

---

## Important: Database Persistence

Free tier PostgreSQL databases **sleep after 15 minutes of inactivity** and take a few seconds to wake up. This is normal.

To avoid this with a paid plan, upgrade to **PostgreSQL Standard** ($15/month).

---

## After Deployment: Making Changes

**To deploy new changes:**

1. Make changes to your code locally
2. Commit and push to GitHub:
```bash
git add -A
git commit -m "Your message"
git push origin main
```

3. Render automatically redeploys within 2 minutes!

---

## Troubleshooting

### Check Build Logs
- In Render Dashboard → Your Web Service → **"Logs"** tab
- Look for errors

### Common Issues

**"ModuleNotFoundError"**
- Add the missing package to `requirements.txt`
- Push to GitHub (auto-deploys)

**"DisallowedHost"**
- Check `ALLOWED_HOSTS` environment variable
- Should be `tilecommerce.onrender.com` (or your custom domain)

**Database Connection Error**
- Verify `DATABASE_URL` is set correctly
- Check database is created in PostgreSQL service
- Wait for database to start if new

**Static Files Not Loading**
- Run: `python manage.py collectstatic --noinput`
- Commit and push changes

### Get Help
- Check Render docs: https://render.com/docs
- Django docs: https://docs.djangoproject.com/
- Render Community: https://render.com/community

---

## Using Your Own Domain (Optional)

1. In your Web Service, go to **"Settings"** → **"Custom Domain"**
2. Enter your domain (e.g., `tilecommerce.com`)
3. Add DNS records as shown
4. Update `ALLOWED_HOSTS` environment variable

---

## Upgrade to a Paid Plan (Optional)

If you want better performance:
- Upgrade Web Service: **$7/month**
- Upgrade Database: **$15/month**

Both are optional - the free tier works fine for testing!

---

**Your TileCommerce site is now live on Render! 🚀**
