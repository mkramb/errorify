import math
import string

def file_size_format(bytes_size, precision=2):
    """Returns a humanized string for a given amount of bytes"""
    bytes_size = int(bytes_size)

    if bytes_size is 0: return '0 bytes'
    log = math.floor(math.log(bytes_size, 1024))

    return "%.*f %s" % (
        precision,
        bytes_size / math.pow(1024, log),
        ['bytes', 'kb', 'mb', 'gb', 'tb','pb', 'eb', 'zb', 'yb']
        [int(log)]
    )

text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
_null_trans = string.maketrans("", "")

def is_text_file(checkfile, blocksize = 512):
    s = checkfile.read(blocksize)

    if "\0" in s:
        return False

    if not s:  # Empty files are considered text
        return True

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return False

    return True
