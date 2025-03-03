import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL for connecting to PostgreSQL
DB_URL = os.getenv('DATABASE_URL')  # Make sure it's set in .env

# Secret key for session management or other security purposes
SECRET_KEY = os.getenv('SECRET_KEY')  # Make sure it's set in .env

# Flask environment configuration
ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Convert string to boolean

# Additional configurations (for example, email, API keys, etc.)
MAIL_SERVER = os.getenv('MAIL_SERVER')  # Ensure to set in .env if needed
MAIL_PORT = os.getenv('MAIL_PORT', 587)  # Default value is 587
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'  # Convert string to boolean

