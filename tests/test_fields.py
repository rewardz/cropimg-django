from cropimg.fields import CIImageField, CIThumbnailField
from cropimg import forms


def test_ci_image_field_formfield_returns_ciimagefield():
    """
    CIImageField should return the custom form field.
    """

    # Arrange
    field = CIImageField()

    # Act
    form_field = field.formfield()

    # Assert
    assert isinstance(form_field, forms.CIImageField)


def test_ci_image_field_formfield_accepts_kwargs():
    """
    CIImageField should pass kwargs to the form field.
    """

    # Arrange
    field = CIImageField()

    # Act
    form_field = field.formfield(required=False)

    # Assert
    assert form_field.required is False


def test_cithumbnailfield_internal_type():
    """
    CIThumbnailField should behave like a CharField internally.
    """

    # Arrange
    field = CIThumbnailField(image_field="img", size=(100, 100))

    # Act
    internal_type = field.get_internal_type()

    # Assert
    assert internal_type == "CharField"


def test_cithumbnailfield_deconstruct_contains_image_field_and_size():
    """
    deconstruct() should preserve image_field and size.
    """

    # Arrange
    field = CIThumbnailField(image_field="img", size=(100, 100))

    # Act
    name, path, args, kwargs = field.deconstruct()

    # Assert
    assert kwargs["image_field"] == "img"
    assert kwargs["size"] == (100, 100)


def test_cithumbnailfield_formfield_returns_cithumbnailfield():
    """
    CIThumbnailField should return the custom thumbnail form field.
    """

    # Arrange
    field = CIThumbnailField(image_field="img", size=(100, 100))

    # Act
    form_field = field.formfield()

    # Assert
    assert isinstance(form_field, forms.CIThumbnailField)


def test_cithumbnailfield_formfield_passes_correct_kwargs():
    """
    Form field should receive name, image_field, and size.
    """

    # Arrange
    field = CIThumbnailField(image_field="img", size=(100, 100))

    # Act
    form_field = field.formfield(name="thumb")

    # Assert
    assert form_field.name == "thumb"
    assert form_field.image_field == "img"
    assert form_field.size == (100, 100)
