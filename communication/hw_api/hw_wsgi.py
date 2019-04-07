from hw_api_flask import application

# WARNING: Currently not in use, as the API has been moved to a wrapper class
# Using Gunicorn in the wrapper is a TODO

# Run me using gunicorn when in production
# Example:
# gunicorn --bind 127.0.0.1:8000 hw_wsgi

if __name__ == "__main__":
    application.run()
