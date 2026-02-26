==============
django cropimg
==============

Django app for generating thumbnails based on easythumbnails and cropimg js library.

.. image:: https://raw.githubusercontent.com/rewardz/cropimg-django/master/screenshots/admin.png 

Main features
-------------

1. **live update**
    You define your thumbnails as soon as you select the image you want to upload without having to upload it first.
2. **cropping flexibility**
    If you have a rectangle image that you want to fit in a square thumbnail, you can totally do that and remaining part of the square will be made transparent.
3. **extra helper buttons**
    That would allow you to center image, align, fit width or fit height

Credits
-------
Most of the ideas and code structure - but not actual code - of this project are based on `Django Image Cropping <https://github.com/jonasundderwolf/django-image-cropping>`_.


A fork of `cropimg <http://requtize.github.io/cropimg/>`_ was used as the Javascript library for selecting thumbnails.


Installation
------------------

1. Add to requirements.txt::
  ``git+https://github.com/rewardz/cropimg-django.git@master#egg=cropimg-django``

2. Include cropimg thumbnail processor in easythumbnails settings (settings.py)

.. code:: python

    from easy_thumbnails.conf import Settings as ThumbnailSettings
    THUMBNAIL_PROCESSORS = (
        'cropimg.thumbnail_processors.crop_box',
    ) + ThumbnailSettings.THUMBNAIL_PROCESSORS
3. Include cropimg to your installed apps (settings.py)

.. code:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        ...
        'cropimg',
    ]

4. Add thumbnail fields to your model

.. code:: python

    from easy_thumbnails.files import get_thumbnailer
    from cropimg.fields import CIImageField, CIThumbnailField

    class MyModel(models.Model):
        my_img = CIImageField(upload_to="images/", blank=True, null=True)
        img_display = CIThumbnailField('my_img', (600, 400), blank=True, null=True)
        img_thumbnail = CIThumbnailField('my_img', (200, 200), blank=True, null=True)

        def get_thumbnail(self, size, value, default_url=""):
            if not self.my_img:
                return default_url
            return get_thumbnailer(self.img).get_thumbnail({
                'size': size,
                'ci_box': value,
            }).url

        def get_display_img_url():
            return self.get_thumbnail((600, 400), self.img_display)

        def get_thumbnail_img_url():
            return self.get_thumbnail((200, 200), self.img_thumbnail)



*CIImageField* accept same paramters as *ImageField* and can replace it without any code change.
*CIThumbnailField* require field_name which you are generating thumbnail for & desired thumbnail size.

5. in admin.py add

.. code:: python

    from cropimg.admin import CIAdminMixin

    class MyModelAdmin(CIAdminMixin, admin.ModelAdmin):

This Mixin will ensure thumbnail fields are rendered properly in admin.

Using with Django tempales
--------------------------
**Note: This library require jQuery and it assumes the library is already loaded.**

1. make sure you've included jQuery in yoru template
2. include your form dependencies ``{form.media}``
3. just render your form as usual ``{{form.as_p}}``

Running docker container in local for Django 1.8
--------------------------
**Build image and run container to run testcases:**

1. ``docker build --target cropimg-django18 -t cropimg-django18 .``

2. ``docker run -it feeds_image:latest``

**RUN below command to enter into docker shell**

``docker run -it --rm cropimg-django18:latest bash``

**Once you're inside docker shell, then Run below commands for test cases:**

``make test``

Makefile Commands
-----------------

The project includes a ``Makefile`` to simplify testing tasks.
All targets are defined as ``.PHONY`` so they always execute when called.

Available commands:

make help
  Displays all available Makefile commands.

make install_django18
  Installs test dependencies required for Django 1.8.

make test
  Runs the complete test suite using pytest.

make test_with_coverage
  Executes the test suite and shows a coverage report in the terminal.

make build_with_django_18
  Build and run docker image with django 1.8

make build_with_django_111_python_37
  Build and run docker image with django 1.11 and python 3.7