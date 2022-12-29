import os
    


from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = os.environ.get('SECRET_KEY')


ALLOWED_HOSTS = ["*"]

CORS_ALLOW_HEADERS = ['*']

CORS_ALLOW_ALL_ORIGINS = True



DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'your-db-name',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': 'mongodb+srv://<username>:<password>@<atlas cluster>/<myFirstDatabase>?retryWrites=true&w=majority'
        }  
    }
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dhw9oa5fm",
    'API_KEY': os.environ.get("API_KEY"),
    'API_SECRET': os.environ.get("API_SECRET"),
}

