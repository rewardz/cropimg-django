from django.db import models
from django import forms
from .widgets import CIThumbnailWidget, CIImgWidget


class CIFormImageField(forms.ImageField):

    widget = CIImgWidget


class CIImageField(models.ImageField):

    def formfield(self, **kwargs):
        defaults = {'form_class': CIFormImageField}
        defaults.update(kwargs)
        return super(CIImageField, self).formfield(**defaults)


class CIThumbnailField(models.CharField):

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
        kwargs["max_length"] = kwargs.get("max_length", 1024)
        super(CIThumbnailField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {"image_field": self.image_field, "thumbnail_field": self.name}

    def deconstruct(self):
        result = super(CIThumbnailField, self).deconstruct()
        result[3].update({"image_field": self.image_field, "size": self.size})
        return result

    def formfield(self, **kwargs):
        kwargs["widget"] = self.widget({
            "form_class": None,
            "data-image-field": self.image_field,
            "data-thumb-field": self.name,
            "data-thumb-size": "%d,%d" % self.size,
            "data-type": "thumbnail_field"
        })
        return super(CIThumbnailField, self).formfield(**kwargs)
