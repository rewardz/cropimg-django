from django.db import models
from cropimg.fields import CIImageField, CIThumbnailField


class CropImgTestModel(models.Model):
    """
    Dummy model used only for testing cropimg model fields.
    """
    img = CIImageField(upload_to="photos")
    thumb = CIThumbnailField(image_field="img", size=(100, 100))

    class Meta:
        app_label = 'cropimg'
