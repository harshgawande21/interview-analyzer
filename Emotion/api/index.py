import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import the app
from app import create_app

app = create_app()

# Vercel expects a WSGI app named `app` or `handler`
# Export the Flask app for Vercel
handler = app

if __name__ == "__main__":
    app.run()
