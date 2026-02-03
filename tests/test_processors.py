from PIL import Image
import pytest

from cropimg.thumbnail_processors import crop_box


def create_image():
    """
    Create a simple test image.
    """
    return Image.new("RGB", (100, 100), (255, 0, 0))


def test_crop_box_no_ci_box():
    """
    Image should remain unchanged when ci_box is False.
    """

    # Arrange
    img = create_image()

    # Act
    result = crop_box(img, (50, 50), ci_box=False)

    # Assert
    assert result.size == img.size


def test_crop_box_valid_ci_box():
    """
    Valid ci_box should crop the image correctly.
    """

    # Arrange
    img = create_image()

    # Act
    result = crop_box(img, (50, 50), ci_box="10,10,20,20")

    # Assert
    assert result.size == (20, 20)


def test_crop_box_invalid_format_raises_value_error():
    """
    Invalid ci_box format should raise ValueError.
    """

    # Arrange
    img = create_image()

    # Act / Assert
    with pytest.raises(ValueError):
        crop_box(img, (50, 50), ci_box="10,10,20")


def test_crop_box_invalid_values_raises_value_error():
    """
    Non-numeric ci_box values should raise ValueError.
    """

    # Arrange
    img = create_image()

    # Act / Assert
    with pytest.raises(ValueError):
        crop_box(img, (50, 50), ci_box="10,abc,20,20")


def test_crop_box_huge_dimensions_ignored():
    """
    Excessively large crop dimensions should be ignored.
    """

    # Arrange
    img = create_image()

    # Act
    result = crop_box(img, (50, 50), ci_box="0,0,10000,10000")

    # Assert
    assert result.size == img.size


def test_crop_box_negative_values_returns_original():
    """
    Negative or invalid values should return original image.
    """

    # Arrange
    img = create_image()

    # Act
    result = crop_box(img, (50, 50), ci_box="-10,-10,-5,-5")

    # Assert
    assert result.size == img.size
