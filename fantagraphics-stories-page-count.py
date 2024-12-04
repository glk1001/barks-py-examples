import argparse

from intspan import intspan

from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir
from barks_fantagraphics.comic_book import get_jpg_page_list

COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"


def get_args():
    parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Create a clean Barks comic from Fantagraphics source."
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

page_count = 0
for title in titles:
    comic_book = comics_database.get_comic_book(title)
    page_count += len(get_jpg_page_list(comic_book))

print(f"{len(titles)} titles, {page_count} pages")
