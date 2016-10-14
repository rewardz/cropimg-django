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
    try:
        x, y, width, height = [int(i) for i in ci_box.split(",")]
    except ValueError as e:
        # try to guess why the exception happened
        values = ci_box.split(",")
        if len(values) != 4:
            raise ValueError("crop_box must contain exactly 4 values x,y,width,height")
        raise ValueError("crop_box processor got the following error"
                         "when processing the value %s\n%s" % (ci_box, e.message))

    if width <= 0 or height <= 0:
        # That's basically an unintialized value
        return im

    # Handle one-dimensional targets.
    im = im.convert("RGBA").crop((x, y, x + width, y + height))
    return im
