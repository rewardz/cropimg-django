import os
from easy_thumbnails.conf import Settings as ThumbnailSettings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "test"
DEBUG = True

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "easy_thumbnails",
    "cropimg",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            "SERIALIZE": False,
        }
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "tests", "templates")],
        "APP_DIRS": True,
    }
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

THUMBNAIL_PROCESSORS = (
    'cropimg.thumbnail_processors.crop_box',
) + ThumbnailSettings.THUMBNAIL_PROCESSORS

THUMBNAIL_ALIASES = {}
