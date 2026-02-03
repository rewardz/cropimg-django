import pytest
from django import forms

from cropimg.forms import CIImageField, CIThumbnailField
from cropimg.widgets import CIImgWidget, CIThumbnailWidget


class TestFieldForm(forms.Form):
    """
    Form used to test custom image and thumbnail fields.
    """
    image = CIImageField()
    thumb = CIThumbnailField(image_field="image", size=(200, 200), name="thumb")


def test_ci_image_field_widget_is_ciimgwidget():
    """
    CIImageField should use CIImgWidget.
    """

    # Arrange
    form = TestFieldForm()

    # Act
    widget = form.fields["image"].widget

    # Assert
    assert isinstance(widget, CIImgWidget)


def test_ci_thumbnail_field_widget_is_cithumbnailwidget():
    """
    CIThumbnailField should use CIThumbnailWidget.
    """

    # Arrange
    form = TestFieldForm()

    # Act
    widget = form.fields["thumb"].widget

    # Assert
    assert isinstance(widget, CIThumbnailWidget)


def test_ci_thumbnail_widget_attrs_are_set_correctly():
    """
    Thumbnail widget should expose required data attributes.
    """

    # Arrange
    form = TestFieldForm()
    field = form.fields["thumb"]
    widget = field.widget

    # Act
    attrs = field.widget_attrs(widget)

    # Assert
    assert attrs["data-image-field"] == "image"
    assert attrs["data-thumb-field"] == "thumb"
    assert attrs["data-thumb-size"] == "200,200"
    assert attrs["data-type"] == "thumbnail_field"
    assert "cropimg-field" in attrs["class"]


def test_ci_thumbnail_field_requires_list_or_tuple():
    """
    Thumbnail size must be a tuple or list.
    """

    # Arrange / Act / Assert
    with pytest.raises(AssertionError):
        CIThumbnailField(image_field="image", size="not-a-tuple")
