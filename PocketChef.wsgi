
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)

# Ensure your project is on the Python path
sys.path.insert(0, "/var/www/PocketChef")

# If your app uses environment variables, define them once here
os.environ['TEST'] = 'test'
os.environ['FACEBOOK_APP'] = 'Your facebook app id'
os.environ['FACEBOOK_SECRET'] = 'Your facebook app secret'

# Import the Flask application
from PocketChef import app as application
