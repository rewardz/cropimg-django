from django.forms.widgets import Input, ClearableFileInput
from django.template.loader import render_to_string


class CIImgWidget(ClearableFileInput):

    def render(self, name, value, attrs=None):
        try:
            attrs["data-value"] = getattr(value, "url", "")
        except ValueError: # attribute has no file associated with it.
            attrs["data-value"] = ""
        return super(CIImgWidget, self).render(name, value, attrs)


class CIThumbnailWidget(Input):

    input_type = "text"

    def render(self, name, value, attrs=None):
        if attrs:
            attrs.update(self.attrs)
            attrs["type"] = "hidden"
        input_field = super(CIThumbnailWidget, self).render(name, value, attrs)
        return render_to_string("cropimg/cropimg_widget.html",
                                {
                                    "name": name, "value": value, "attrs": attrs,
                                    "input_field": input_field
                                })

    class Media:
        js = ("cropimg/js/jquery_init.js", "cropimg/js/cropimg.jquery.js",
              "cropimg/js/cropimg_init.js")
        css = {"all": ["cropimg/resource/cropimg.css"]}
