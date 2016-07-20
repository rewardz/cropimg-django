from django.contrib import admin
from cropimg.fields import CIImageField
from cropimg.widgets import CIImgWidget
from .models import SimpleModel


class CIAdminMixin(object):

    def formfield_for_dbfield(self, db_field, **kwargs):
        form_field = super(CIAdminMixin, self).formfield_for_dbfield(db_field, **kwargs)
        if isinstance(db_field, CIImageField):
            form_field.widget = CIImgWidget()
        return form_field

