import argparse
import unicodedata

import textgrid
from textgrid import IntervalTier
from textgrid import Interval


def clean_mark(mark):
    """

    replace each accented letter with a capital letter
    use the same values as the original interval
    except that each accented letter with be
    replaced by a capital letter

    >>> clean_mark(u"\U000000E1")
    'A'

    >>> clean_mark(u"\U000000E9")
    'E'

    >>> clean_mark(u"\U000000ED")
    'I'

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

    NFKD_normalized_mark = unicodedata.normalize('NFKD', mark)

    stripped_combining_mark = "".join(
        [c for c in NFKD_normalized_mark if not unicodedata.combining(c)])

    ascii_encoded_mark = stripped_combining_mark.encode('ascii')
    utf8_decoded_mark = ascii_encoded_mark.decode("utf-8")

    cleaned_mark = utf8_decoded_mark

    if cleaned_mark == mark:
        return mark
    else:
        return cleaned_mark.upper()


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
    # parser.add_argument('--dest-file',
    #                     type=argparse.FileType('w', encoding='UTF-8'))
    args = parser.parse_args()

    #print(args.source_file)
    #print(args.dest_file)

    source_tg = textgrid.TextGrid()
    source_tg.read(f=args.source_file)

    cleaned_tg = remove_accents(source_tg)

    with open(args.dest_file, "w") as f:
        cleaned_tg.write(f)

    #cleaned_tg.write(args.dest_file)
    print("done")
    #remove_accents()
