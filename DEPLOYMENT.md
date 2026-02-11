# Heroku Deployment Guide for TileCommerce

## Prerequisites
1. A free Heroku account (create at https://www.heroku.com)
2. Heroku CLI installed (download from https://devcenter.heroku.com/articles/heroku-cli)
3. Git installed

## Step-by-Step Deployment Instructions

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit - ready for Heroku deployment"
```

### 2. Create Heroku Account and App
- Go to https://www.heroku.com and sign up
- Create a new app from the Heroku dashboard or via CLI:
```bash
heroku login
heroku create your-app-name
```
(Replace `your-app-name` with a unique name, or leave blank for auto-generated)

### 3. Add Heroku Postgres Database
```bash
heroku addons:create heroku-postgresql:essential-0
```

### 4. Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY='your-new-secret-key-here'
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
```

Generate a secure secret key:
- Option A: Use Python
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Option B: Use an online tool like https://www.miniwebtool.com/django-secret-key-generator/

### 5. Run Database Migrations on Heroku
```bash
heroku run python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
heroku run python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Deploy Your App
```bash
git push heroku main
```
(If your main branch is called `master`, use `git push heroku master` instead)

### 9. View Your Live App
```bash
heroku open
```

Your app is now live at: `https://your-app-name.herokuapp.com`

## Common Commands

### Check Logs
```bash
heroku logs --tail
```

### Access Heroku Shell
```bash
heroku run python manage.py shell
```

### Update After Making Changes Locally
```bash
git add .
git commit -m "Your changes"
git push heroku main
heroku run python manage.py migrate  # If you changed models
```

### Scale Dynos (if needed on paid plan)
```bash
heroku ps:scale web=1
```

## Troubleshooting

### Issue: "Push rejected, failed to compile the app"
- Check logs: `heroku logs --tail`
- Ensure `Procfile` exists in root directory
- Ensure `requirements.txt` is up to date

### Issue: Database connection errors
- Verify DATABASE_URL is set: `heroku config`
- Run migrations: `heroku run python manage.py migrate`

### Issue: Static files not loading
- Collect static files: `python manage.py collectstatic --noinput`
- Check STATIC_ROOT in settings.py

### Issue: Custom domain name
```bash
heroku domains:add www.yourdomain.com
# Then configure DNS settings with your domain provider
```

## Notes
- **Free Tier Changes**: Heroku discontinued the free tier in November 2022. Basic paid dynos (~$7/month) are now required.
- **Database**: Heroku Postgres essential plans start at ~$9/month or you can use the free tier with limitations.
- **Media Files**: For user uploads, consider using AWS S3 or Cloudinary instead of local storage.
