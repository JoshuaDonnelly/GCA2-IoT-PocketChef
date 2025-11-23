
import sys
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stderr)

# Make sure project directory is on path
sys.path.insert(0, "/var/www/PocketChef")

# Load environment variables
load_dotenv("/var/www/PocketChef/.env")

from PocketChef import app as application

