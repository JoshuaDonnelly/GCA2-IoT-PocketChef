import sys
import os
import logging

# Add logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Add your project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

print(f"DEBUG: Python path: {sys.path}", file=sys.stderr)
print(f"DEBUG: Current directory: {os.getcwd()}", file=sys.stderr)

try:
    # Set environment variables if needed
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_dir, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print("DEBUG: Environment variables loaded", file=sys.stderr)
    else:
        print("DEBUG: No .env file found", file=sys.stderr)
    
    # Import your Flask application
    from PocketChef import app as application
    print("DEBUG: Flask app imported successfully", file=sys.stderr)
    
except Exception as e:
    print(f"DEBUG: Error importing app: {str(e)}", file=sys.stderr)
    import traceback
    print(f"DEBUG: Traceback: {traceback.format_exc()}", file=sys.stderr)
    raise

if __name__ == "__main__":
    application.run()
