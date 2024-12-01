import argparse

from intspan import intspan

from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir
from barks_fantagraphics.comics_utils import get_abbrev_jpg_page_list

COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"


def get_args():
    parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Get Barks titles in Fantagraphics volumes."
    )

    parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    parser.add_argument(
        VOLUME_ARG,
        action="store",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    return args


cmd_args = get_args()
comics_database = ComicsDatabase(cmd_args.comics_database_dir)
vol_list = list(intspan(cmd_args.volume))

titles = comics_database.get_all_story_titles_in_fantagraphics_volume(vol_list)
max_len = max([len(title) for title in titles])

for title in titles:
    comic_book = comics_database.get_comic_book(title)
    print(f'Title: "{title:<{max_len}}", jpgs: {", ".join(get_abbrev_jpg_page_list(comic_book))}')
