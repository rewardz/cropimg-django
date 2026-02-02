from django import forms

from cropimg.widgets import CIImgWidget, CIThumbnailWidget


class TestWidgetForm(forms.Form):
    """
    Form used to test widget rendering and media.
    """
    image = forms.ImageField(widget=CIImgWidget())
    crop = forms.CharField(widget=CIThumbnailWidget())


def test_ci_img_widget_renders_file_input():
    """
    CIImgWidget should render a file input.
    """

    # Arrange
    widget = CIImgWidget()

    # Act
    html = widget.render("image", None, attrs={})

    # Assert
    assert 'type="file"' in html
    assert 'data-value="' in html


def test_ci_img_widget_value_error_case():
    """
    Widget should handle values without an attached file.
    """

    # Arrange
    widget = CIImgWidget()

    class TestValue(object):
        def __bool__(self):
            return False

        def __nonzero__(self):
            return False

        def __getattr__(self, name):
            raise ValueError("no file")

    value = TestValue()

    # Act
    html = widget.render("image", value, attrs={})

    # Assert
    assert 'data-value=""' in html


def test_ci_thumbnail_widget_renders_hidden_input():
    """
    CIThumbnailWidget should render a hidden input with preview image.
    """

    # Arrange
    widget = CIThumbnailWidget()

    # Act
    html = widget.render("thumb", "", attrs={"class": "test"})

    # Assert
    assert 'type="hidden"' in html
    assert '<img' in html
    assert 'id="-img"' in html


def test_form_media_includes_js_and_css():
    """
    Widget media should include required JS and CSS.
    """

    # Arrange
    form = TestWidgetForm()

    # Act
    media_html = form.media.__str__()

    # Assert
    assert "cropimg/js/cropimg.jquery.js" in media_html
    assert "cropimg/js/cropimg_init.js" in media_html
    assert "cropimg/resource/cropimg.css" in media_html
