==============
django cropimg
==============

Django app for generating thumbnails based on easythumbnails and cropimg js library.

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
  ``git+https://github.com/rewardz/cropimg-django.git@master#egg=cropimg-django django-model-helpers==1.2.1``

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

    from cropimg.fields import CIImageField, CIThumbnailField

    class MyModel(models.Model):
        my_img = CIImageField(upload_to="images/", blank=True, null=True)
        img_display = CIThumbnailField('my_img', (600, 400), blank=True, null=True)
        img_thumbnail = CIThumbnailField('my_img', (200, 200), blank=True, null=True)


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
