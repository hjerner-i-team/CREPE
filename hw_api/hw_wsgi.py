from hw_api import application

# Run me using gunicorn when in production
# Example:
# gunicorn --bind 127.0.0.1:8000 hw_wsgi

if __name__ == "__main__":
    application.run()
