import argparse

import textgrid
from textgrid import IntervalTier
from textgrid import Interval


def clean_mark(mark):
    return mark.upper()


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

    # for tier in textgrid:
    #     for interval in tier:
    #         for letter in interval:
    #             """
    #             replace each accented letter with a capital letter
    #             use the same values as the original interval
    #             except that each accented letter with be
    #             replaced by a capital letter
    #             """
    #             letter.replace("U+00E1", "A")
    #             letter.replace("U+00E9", "E")
    #             letter.replace("U+00ED", "I")
    #             letter.replace("U+00F3", "O")
    #             letter.replace("U+00FA", "U")
    #             letter.replace("U+00C1", "A")
    #             letter.replace("U+00C9", "E")
    #             letter.replace("U+00CD", "I")
    #             letter.replace("U+00D3", "O")
    #             letter.replace("U+00DA", "U")
    #             letter.replace("U+00F1", "N")
    #             letter.replace("U+00D1", "N")
    #     #once each interval has been cleaned
    #     #return the cleaned product!

    # # does this need to be here since it would just work by
    # # going into the directory and changing everything
    # # within the directory
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
