try:
    from PIL import Image
except ImportError:
    import Image


def crop_box(im, size, box=False, **kwargs):
    """
    Crop image based on very specific pixel values (x,y,width,height)

    box
        Crop the source image to exactly match the requested box
    """
    if not box:
        return im

    assert isinstance(box, basestring)
    if box.count(",") != 3:
        raise ValueError("box must contain exactly 4 values x,y,width,height")
    x, y, width, height = [int(i) for i in box.split(",")]
    # Handle one-dimensional targets.
    im = im.convert("RGBA").crop((x, y, x + width, y + height))
    return im
