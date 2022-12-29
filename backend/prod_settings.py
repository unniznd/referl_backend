
from dotenv import load_dotenv
import os

load_dotenv()


from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ.get('SECRET_KEY')


ALLOWED_HOSTS = ["*"]

CORS_ALLOW_HEADERS = ['*']

CORS_ALLOW_ALL_ORIGINS = True



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'referldb',
        'USER': 'unnikuznd',
        'PASSWORD': os.getenv("PASSWORD"),
        'HOST':'unnikuznd.mysql.pythonanywhere-services.com',
        'PORT':'3306',
    }
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dhw9oa5fm",
    'API_KEY': os.getenv("API_KEY"),
    'API_SECRET': os.getenv("API_SECRET"),
}

