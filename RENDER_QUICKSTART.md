# Render Deployment - Quick Start

## 3 Simple Steps to Deploy

### 1. Create Account & Connect GitHub
- Go to https://render.com
- Sign up with GitHub
- Authorize Render to access your repositories

### 2. Deploy Web Service
- Click **"+ New"** → **"Web Service"**
- Select `CodingPersonality/TileCommerce`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn TileCommerce.wsgi:application`
- **Plan**: Free
- Click **"Deploy"**

### 3. Create Database
- Click **"+ New"** → **"PostgreSQL"**
- **Name**: `tilecommerce-db`
- **Plan**: Free
- Copy the **Internal Database URL**
- Go back to Web Service → **Environment**
- Add: `DATABASE_URL` = (paste the URL)

### 4. Add Secret Key
Run locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add to Web Service **Environment**:
- `SECRET_KEY` = (paste generated key)
- `DEBUG` = `False`

### Done! 🎉
Your site is live at: `https://tilecommerce.onrender.com`

---

## After Deployment
Every time you push to GitHub:
```bash
git push origin main
```
→ Render automatically redeploys!

---

See **RENDER_DEPLOYMENT.md** for detailed instructions.
