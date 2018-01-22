import codecs
import locale
import re
import sys

BOMS = [
    (codecs.BOM_UTF8, 'utf8'),
    (codecs.BOM_UTF16, 'utf16'),
    (codecs.BOM_UTF16_BE, 'utf16-be'),
    (codecs.BOM_UTF16_LE, 'utf16-le'),
    (codecs.BOM_UTF32, 'utf32'),
    (codecs.BOM_UTF32_BE, 'utf32-be'),
    (codecs.BOM_UTF32_LE, 'utf32-le'),
]

ENCODING_RE = re.compile(br'coding[:=]\s*([-\w.]+)')


def auto_decode(data):
    """Check a bytes string for a BOM to correctly detect the encoding

    Fallback to locale.getpreferredencoding(False) like open() on Python3"""
    for bom, encoding in BOMS:
        if data.startswith(bom):
            return data[len(bom):].decode(encoding)
    # Lets check the first two lines as in PEP263
    for line in data.split(b'\n')[:2]:
        if line[0:1] == b'#' and ENCODING_RE.search(line):
            encoding = ENCODING_RE.search(line).groups()[0].decode('ascii')
            return data.decode(encoding)
    return data.decode(
        locale.getpreferredencoding(False) or sys.getdefaultencoding(),
    )


def fs_decode(data):
    """Wrapper around data.decode() using filesystem encoding

    sys.getfilesystemencoding() may return `None` which may cause issues when
    it is used as an argument for s.decode()."""
    fs_enc = sys.getfilesystemencoding() or 'ascii'
    return data.decode(fs_enc)


def fs_encode(data):
    """Wrapper around data.encode() using filesystem encoding

    sys.getfilesystemencoding() may return `None` which may cause issues when
    it is used as an argument for s.encode()."""
    fs_enc = sys.getfilesystemencoding() or 'ascii'
    return data.encode(fs_enc)
