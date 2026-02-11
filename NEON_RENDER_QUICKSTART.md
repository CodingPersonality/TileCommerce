# Render + Neon Quick Start

## TL;DR - Deploy in 3 Steps

### Step 1: Get Neon Database URL
- Go to https://neon.tech → Sign Up → Create Project
- Copy your connection string
- Save it somewhere (you'll need it in 2 minutes)

### Step 2: Deploy on Render
- Go to https://render.com → Sign Up with GitHub
- Click **"+ New"** → **"Web Service"**
- Connect your GitHub: `CodingPersonality/TileCommerce`
- Set:
  - Build: `./build.sh`
  - Start: `gunicorn TileCommerce.wsgi:application`
  - Plan: `Free`

### Step 3: Add Secrets
In Render under **"Advanced"** → **"Environment"**, add:
```
DATABASE_URL = (paste your Neon URL from Step 1)
SECRET_KEY = (run locally: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
PYTHON_VERSION = 3.10.13
DEBUG = False
```

### Done! ✅
- Click **"Deploy"**
- Wait 5 minutes
- Visit: `https://tilecommerce.onrender.com`

---

## Why This Works

✅ **Neon** = Your database (free, permanent)
✅ **Render** = Your website (free hosting)
✅ **GitHub** = Your code (automatic deployments)

When you `git push`, Render automatically redeploys!

---

## See NEON_RENDER_GUIDE.md for Detailed Steps
