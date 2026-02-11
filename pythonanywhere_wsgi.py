# PythonAnywhere WSGI configuration
# Place this in PythonAnywhere's Web app configuration under WSGI configuration file

import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/TileCommerce'  # Replace with your PythonAnywhere username
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'TileCommerce.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
