# PythonAnywhere Deployment Guide for TileCommerce

## Step 1: Create a PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Click "Sign up" and create a new account (free tier available)
3. Verify your email address

## Step 2: Set Up Your Web App on PythonAnywhere

1. Log in to your PythonAnywhere Dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" (not using a framework option)
4. Select **Python 3.10** (or the version you prefer)
5. Complete the setup - this creates a basic web app

## Step 3: Configure Your Git Repository

1. Open a **Bash console** on PythonAnywhere (Consoles tab)
2. Clone your GitHub repository:
   ```bash
   git clone https://github.com/yourusername/TileCommerce.git
   cd TileCommerce
   ```

3. Create a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Step 4: Create Your PostgreSQL Database on PythonAnywhere

1. Go to **Databases** tab on PythonAnywhere
2. Click "Create a new database"
3. Choose **PostgreSQL**
4. The database will be created automatically (no password needed for free tier)
5. Note your database credentials:
   - Server: `yourusername.postgres.pythonanywhere-services.com`
   - Database name: `yourusername$tilecommerce`
   - Username: `yourusername`
   - Password: (shown in the databases tab)

## Step 5: Configure Environment Variables

1. Create a `.env` file in your project root: `/home/yourusername/TileCommerce/`
   ```bash
   nano ~/TileCommerce/.env
   ```

2. Add the following (replace YOUR values):
   ```
   DEBUG=False
   SECRET_KEY=your-generated-secret-key-here
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   DATABASE_URL=postgres://yourusername:your_db_password@yourusername.postgres.pythonanywhere-services.com/yourusername$tilecommerce
   ```

3. Press `Ctrl+X`, then `Y`, then `Enter` to save

## Step 6: Generate a Secure Secret Key

In the Bash console:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key and update your `.env` file with it.

## Step 7: Migrate the Database

In your Bash console:
```bash
cd ~/TileCommerce
source venv/bin/activate
python manage.py migrate --noinput
```

## Step 8: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## Step 9: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 10: Configure the WSGI Configuration File

1. Go to **Web** tab on PythonAnywhere
2. Click on your web app
3. Scroll down to **"Code"** section
4. Open the **"WSGI configuration file"** (paste the path shown there)
5. Replace the entire content with this (from your `pythonanywhere_wsgi.py`):

```python
import os
import sys
import django
from pathlib import Path

# Add your project directory to the sys.path
path = '/home/yourusername/TileCommerce'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TileCommerce.settings')

# Load .env file
env_file = os.path.join(path, '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value

# Setup Django
django.setup()

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Save the file

## Step 11: Update Virtual Environment Path

1. Still in the **Web** tab for your app
2. Look for **"Virtualenv"** section
3. Click "Enter path to a virtualenv"
4. Enter: `/home/yourusername/TileCommerce/venv`
5. Press Enter

## Step 12: Configure Static and Media Files

1. In the **Web** tab, scroll to **"Static files"**
2. Add these mappings:

   | URL | Directory |
   |-----|-----------|
   | /static/ | /home/yourusername/TileCommerce/staticfiles |
   | /media/ | /home/yourusername/TileCommerce/media |

3. Click "Save"

## Step 13: Reload Your Web App

1. Still in the **Web** tab
2. Click the big green **"Reload"** button at the top
3. Wait 10-20 seconds for the app to reload

## Step 14: Test Your Deployment

1. Visit: `https://yourusername.pythonanywhere.com`
2. Your website should now be live!
3. Access admin panel at: `https://yourusername.pythonanywhere.com/admin`

## Troubleshooting

### Check Error Logs
- Go to **Web** tab
- Scroll to **"Log files"**
- Check "Error log" and "Server log" for any errors

### Common Issues

**ModuleNotFoundError:**
- Ensure virtual environment is correctly set
- Check that all packages in `requirements.txt` are installed

**Database Connection Error:**
- Verify DATABASE_URL in `.env` file
- Check database credentials in PythonAnywhere **Databases** tab
- Ensure database was created

**Static Files Not Loading:**
- Run `python manage.py collectstatic --noinput` again
- Check the static files mapping in **Web** tab

**ImportError for `.env`:**
- Install `python-dotenv` if not in requirements.txt:
  ```bash
  pip install python-dotenv
  ```

### Getting Help

- Check the error log in **Web** > **Log files**
- Visit https://www.pythonanywhere.com/forums/ for support
- Django documentation: https://docs.djangoproject.com/

---

## After Deployment: Updating Your Site

To update your site after making changes:

1. Open Bash console
2. Navigate to your project: `cd ~/TileCommerce`
3. Pull latest changes: `git pull origin main`
4. Install any new dependencies: `pip install -r requirements.txt`
5. Run migrations (if database schema changed): `python manage.py migrate`
6. Collect static files: `python manage.py collectstatic --noinput`
7. Reload web app from the **Web** tab

---

**You're all set! Your TileCommerce site is now live on PythonAnywhere!**
