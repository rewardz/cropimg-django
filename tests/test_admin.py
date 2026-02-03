from django.contrib import admin
from django.test import RequestFactory

from cropimg.admin import CIAdminMixin
from tests.models import CropImgTestModel
from cropimg.widgets import CIImgWidget


class CropImgTestModelAdmin(CIAdminMixin, admin.ModelAdmin):
    """
    Dummy ModelAdmin used to test CIAdminMixin behavior.
    """
    pass


def test_ciadminmixin_changes_widget(db):
    """
    Ensure CIAdminMixin replaces the widget for CIImageField.
    """

    # Arrange
    admin_site = admin.AdminSite()
    ma = CropImgTestModelAdmin(CropImgTestModel, admin_site)
    request = RequestFactory().get("/admin/")

    # Act
    form = ma.get_form(request)()
    widget = form.fields["img"].widget

    # Assert
    assert isinstance(widget, CIImgWidget)
