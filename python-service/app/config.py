import os
from dotenv import load_dotenv

load_dotenv()

# Database URL for connecting to PostgreSQL
DB_URL = os.getenv('DATABASE_URL')  

# Database URL for connecting to PostgreSQL (Flask-SQLAlchemy expects this key)
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# Secret key for session management or other security purposes
SECRET_KEY = os.getenv('SECRET_KEY')  

# Flask environment configuration
ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'True') == 'True'  

# Additional configurations (for example, email, API keys, etc.)
MAIL_SERVER = os.getenv('MAIL_SERVER')  
MAIL_PORT = os.getenv('MAIL_PORT', 587)  
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True' 

