import argparse
import unicodedata

import textgrid
from textgrid import IntervalTier
from textgrid import Interval


def clean_char(char):
    """
    replace accented letter with a capital letter.

    >>> clean_char(u"\U000000E1")
    'A'

    >>> clean_char(u"\U000000E9")
    'E'

    >>> clean_char(u"\U000000ED")
    'I'

    >>> clean_char(u"\U000000F3")
    'O'

    >>> clean_char(u"\U000000FA")
    'U'

    >>> clean_char(u"\U000000C1")
    'A'

    >>> clean_char(u"\U000000C9")
    'E'

    >>> clean_char(u"\U000000CD")
    'I'

    >>> clean_char(u"\U000000D3")
    'O'

    >>> clean_char(u"\U000000DA")
    'U'

    >>> clean_char(u"\U000000F1")
    'N'

    >>> clean_char(u"\U000000D1")
    'N'

    >>> clean_char("A")
    'A'

    >>> clean_char("b")
    'b'

    """

    NFKD_normalized_char = unicodedata.normalize('NFKD', char)

    stripped_combining_char = "".join(
        [c for c in NFKD_normalized_char if not unicodedata.combining(c)])

    ascii_encoded_char = stripped_combining_char.encode('ascii')
    utf8_decoded_char = ascii_encoded_char.decode("utf-8")

    cleaned_char = utf8_decoded_char

    if cleaned_char == char:
        return char
    else:
        return cleaned_char.upper()


def clean_mark(mark):
    """
    >>> clean_mark(u"\U000000E1\U00000061")
    'Aa'

    >>> clean_mark(u"\U000000E9\U00000062")
    'Eb'

    >>> clean_mark(u"\U00000061\U000000ED\U00000064\U00000061")
    'aIda'

    >>> clean_mark(u"\U000000F3")
    'O'

    >>> clean_mark(u"\U000000FA")
    'U'

    >>> clean_mark(u"\U000000C1")
    'A'

    >>> clean_mark(u"\U000000C9")
    'E'

    >>> clean_mark(u"\U000000CD")
    'I'

    >>> clean_mark(u"\U000000D3")
    'O'

    >>> clean_mark(u"\U000000DA")
    'U'

    >>> clean_mark(u"\U000000F1")
    'N'

    >>> clean_mark(u"\U000000D1")
    'N'

    >>> clean_mark("A")
    'A'

    >>> clean_mark("b")
    'b'

    """

    return "".join([clean_char(c) for c in mark])


def clean_interval(old_interval):
    new_interval = Interval(minTime=old_interval.minTime,
                            maxTime=old_interval.maxTime,
                            mark=clean_mark(old_interval.mark))
    return new_interval


def clean_tier(old_tier):
    new_tier = IntervalTier(name=old_tier.name)

    for interval in iter(old_tier):
        new_tier.addInterval(clean_interval(interval))

    return new_tier


def remove_accents(source_tg):

    print(source_tg.getNames())

    dest_tg = textgrid.TextGrid()
    for tier in source_tg.getNames():
        dest_tg.tiers.append(clean_tier(source_tg.getFirst(tier)))

    return dest_tg


if __name__ == "__main__":
    description = ("Replace diacritical marks with corresponding "
                   "ASCII CAPS in Praat .TextGrid files")
    parser = argparse.ArgumentParser(usage=None, description=description)

    parser.add_argument('--source-file', type=str)
    parser.add_argument('--dest-file', type=str)
    parser.add_argument('--force',
                        action="store_true",
                        default=False,
                        help=("force replacement, even on non-TextGrid files"))

    args = parser.parse_args()

    if args.force:
        with open(args.source_file, "r") as sf:
            with open(args.dest_file, "w") as df:
                for l in sf.readlines():
                    df.write(clean_mark(l))

    else:
        source_tg = textgrid.TextGrid()
        source_tg.read(f=args.source_file)
        cleaned_tg = remove_accents(source_tg)
        with open(args.dest_file, "w") as f:
            cleaned_tg.write(f)
