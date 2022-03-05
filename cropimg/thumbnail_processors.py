import logging
logger = logging.getLogger("cropimg")


def crop_box(im, size, ci_box=False, **kwargs):
    """
    Crop image based on very specific pixel values (x,y,width,height)

    ci_box
        Crop the source image to exactly match the requested box
    """
    if not ci_box:
        return im

    assert isinstance(ci_box, str)
    try:
        x, y, width, height = [int(i) for i in ci_box.split(",")]
    except ValueError as ex:
        # try to guess why the exception happened
        values = ci_box.split(",")
        if len(values) != 4:
            raise ValueError("crop_box must contain exactly 4 values x,y,width,height")
        raise ValueError("crop_box processor got the following error"
                         "when processing the value %s\n%s" % (ci_box, ex.message))

    if min(width, height, width + x + 1, height + y + 1) <= 0:
        # Uninitialized or meaningless value
        return im

    # Prevent running out of memory in case of huge value for thumbnail box size (i.e 0,0,117334,117334)
    if x + width > im.size[0] * 2 or y + height > im.size[1] * 2:
        logger.warn("Ignoring thumbnail dimensions %s, thumbnail too large", ci_box)
        return im

    # Handle one-dimensional targets.
    im = im.convert("RGBA").crop((x, y, x + width, y + height))
    return im
