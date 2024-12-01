import argparse

from barks_fantagraphics.comics_database import ComicsDatabase, get_default_comics_database_dir

COMICS_DATABASE_DIR_ARG = "--comics-database-dir"


def get_args():
    parser = argparse.ArgumentParser(
        #            prog="build-barks",
        description="Create all required Fantagraphics directories."
    )

    parser.add_argument(
        COMICS_DATABASE_DIR_ARG,
        action="store",
        type=str,
        default=get_default_comics_database_dir(),
    )

    args = parser.parse_args()

    return args


cmd_args = get_args()
comics_database = ComicsDatabase(cmd_args.comics_database_dir)

comics_database.make_all_fantagraphics_directories()
