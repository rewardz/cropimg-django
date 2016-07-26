from django.db import models
import forms
from .widgets import CIThumbnailWidget


class CIImageField(models.ImageField):

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CIImageField}
        defaults.update(kwargs)
        return super(CIImageField, self).formfield(**defaults)


class CIThumbnailField(models.Field):

    widget = CIThumbnailWidget

    def __init__(self, image_field, size, *args, **kwargs):
        """
        :param image_field: name of the image field you are generating thumbnail for
        :type image_field: str
        :param size:
        :type size: None | tuple | list
        """
        assert isinstance(size, (list, tuple)), "Size must be either tuple or list of two items"
        self.image_field = image_field
        self.size = size
        kwargs["max_length"] = kwargs.get("max_length", 30)
        super(CIThumbnailField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        result = super(CIThumbnailField, self).deconstruct()
        result[3].update({"image_field": self.image_field, "size": self.size})
        return result

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {
            "name": self.name,
            "image_field": self.image_field,
            "size": self.size,
            "form_class": forms.CIThumbnailField
        }
        defaults.update(kwargs)
        return super(CIThumbnailField, self).formfield(**defaults)
