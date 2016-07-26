from django import forms
from cropimg.widgets import CIImgWidget, CIThumbnailWidget


class CIImageField(forms.ImageField):

    widget = CIImgWidget


class CIThumbnailField(forms.CharField):

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
        self.name = kwargs.pop("name", "")
        defaults = {"widget": self.widget}
        defaults.update(kwargs)
        super(CIThumbnailField, self).__init__(*args, **defaults)

    def widget_attrs(self, widget):
        attrs = super(CIThumbnailField, self).widget_attrs(widget)
        attrs.update({
            "data-image-field": self.image_field,
            "data-thumb-field": self.name,
            "data-thumb-size": "%d,%d" % self.size,
            "data-type": "thumbnail_field",
            "class": "cropimg-field"
        })
        return attrs
