import argparse

from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir

COMICS_DATABASE_DIR_ARG = "--comics-database-dir"
TITLE_ARG = "--title"


def get_args():
    parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Verify Barks title."
    )

    parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )
    parser.add_argument(
        TITLE_ARG,
        action="store",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    return args


cmd_args = get_args()
comics_database = ComicsDatabase(cmd_args.comics_database_dir)
title = cmd_args.title

found, close = comics_database.is_story_title(title)
if found:
    print(f'This is a valid title: "{title}.')
elif close:
    print(f'"{title}" is not a valid title. Did you mean: "{close}".')
else:
    print(f'"{title}" is not a valid title. Cannot find anything close to this.')
