"""
A simplistic ASCII-art generator that maps pixel brightness values to a set of
ASCII characters.
"""

from PIL import Image

pixel_chars = ['#', 'O', 'o', '.', ' ']
inverted_pixel_chars = list(reversed(pixel_chars))

def to_char(val, invert=False):
    """
    Map a pixel brightness value [0,255] to some ASCII representation
    """
    chars = invert and inverted_pixel_chars or pixel_chars
    i = int(val/256 * len(chars))
    return chars[i]

def _maybe_resize(im, max_w, max_h):

    w, h = im.size
    if w > max_w or h > max_h:
        ratio = min(max_w / w, max_h / h)
        im = im.resize((int(w * ratio), int(h * ratio)))
    return im

def _normalize_image(im, max_size=None):
    w, h = im.size
    if max_size:
        max_w, max_h = max_size
        im = _maybe_resize(im, max_w, max_h)
    return im.convert('L') # grayscale

def to_ascii(source, max_size=None, invert_colors=False):
    """
    Load image data from source (string buffer, file pointer, etc.) and convert
    it to an ASCII string representation.
    """
    im = _normalize_image(Image.open(source), max_size)
    chars = [to_char(val, invert_colors) for val in im.getdata()]
    w, _ = im.size
    return '\n'.join([''.join(chars[i:i+w]) for i in range(0, len(chars), w)])


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-i', '--invert', action='store_true', dest='invert')
    opts, args = parser.parse_args()
    for path in args:
        print(to_ascii(path, max_size=(80,80), invert_colors=opts.invert))
