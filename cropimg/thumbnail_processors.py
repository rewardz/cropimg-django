try:
    from PIL import Image
except ImportError:
    import Image


def crop_box(im, size, ci_box=False, **kwargs):
    """
    Crop image based on very specific pixel values (x,y,width,height)

    ci_box
        Crop the source image to exactly match the requested box
    """
    if not ci_box:
        return im

    assert isinstance(ci_box, basestring)
    if ci_box.count(",") != 3:
        raise ValueError("ci_box must contain exactly 4 values x,y,width,height")
    x, y, width, height = [int(i) for i in ci_box.split(",")]
    # Handle one-dimensional targets.
    im = im.convert("RGBA").crop((x, y, x + width, y + height))
    return im
