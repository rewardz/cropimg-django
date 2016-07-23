from django.forms.widgets import Input, ClearableFileInput
from django.shortcuts import render


class CIImgWidget(ClearableFileInput):

    def render(self, name, value, attrs=None):
        attrs["data-value"] = value.url if value else ""
        return super(CIImgWidget, self).render(name, value, attrs)


class CIThumbnailWidget(Input):

    input_type = "text"

    def render(self, name, value, attrs=None):
        if attrs:
            attrs.update(self.attrs)
            attrs["type"] = "hidden"
        input_field = super(CIThumbnailWidget, self).render(name, value, attrs)
        return render(None, "cropimg/cropimg_widget.html",
                      context={
                          "name": name, "value": value, "attrs": attrs,
                          "input_field": input_field}).content

    class Media:
        js = ("cropimg/js/jquery_init.js", "cropimg/js/cropimg.jquery.js",
              "cropimg/js/cropimg_init.js")
        css = {"all": ["cropimg/resource/cropimg.css"]}
