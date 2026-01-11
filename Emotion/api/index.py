from app import app

# Vercel expects a WSGI app named `app` or `handler`
# Export the Flask app for Vercel
handler = app

if __name__ == "__main__":
    app.run()
