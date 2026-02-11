# Quick Start: TileCommerce Deployment to PythonAnywhere

## Prerequisites
- GitHub account with TileCommerce repository
- PythonAnywhere account (free tier available)

## Quick Steps
1. Sign up at https://www.pythonanywhere.com
2. Add a new web app → Manual Configuration → Python 3.10
3. Open Bash console and clone your repo
4. Create virtual environment and install requirements
5. Set up MySQL database in PythonAnywhere
6. Configure environment variables in .env file
7. Run migrations and collect static files
8. Update WSGI configuration file
9. Reload the web app

## Your Database Info (from PythonAnywhere)
- Server: `yourusername.mysql.pythonanywhere-services.com`
- Database: `yourusername$yourdbname`
- Username: `yourusername`

## .env Template
```
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=mysql://yourusername:password@yourusername.mysql.pythonanywhere-services.com/yourusername$dbname
```

## Important Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Contact Support
- PythonAnywhere Help: https://www.pythonanywhere.com/help/
- Django Docs: https://docs.djangoproject.com/

Detailed guide: See DEPLOYMENT_GUIDE.md
