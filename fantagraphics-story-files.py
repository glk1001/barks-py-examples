import argparse

from intspan import intspan

from barks_fantagraphics.comics_consts import PageType
from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir

STORY_PAGE_TYPES = [
    PageType.FRONT,
    PageType.COVER,
    PageType.BODY,
    PageType.FRONT_MATTER,
    PageType.BACK_MATTER,
]

COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
VOLUME_ARG = "--volume"


def get_args():
    parser = argparse.ArgumentParser(
        description="List all files needed from a Fantagraphics volume."
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

for title in titles:
    comic_book = comics_database.get_comic_book(title)

    srce_files = comic_book.get_final_srce_story_files(STORY_PAGE_TYPES)

    print(title)
    for srce_file in srce_files:
        print(f'    "{srce_file[0]}"')
    print()
