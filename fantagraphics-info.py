import logging
import sys

from barks_fantagraphics.comic_book import get_abbrev_jpg_page_list, get_safe_title
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_utils import setup_logging

setup_logging(logging.INFO)

cmd_args = CmdArgs("Fantagraphics info", CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

comics_database = cmd_args.get_comics_database()

titles = cmd_args.get_titles()
max_len = max([len(title) for title in titles])

for title in titles:
    comic_book = comics_database.get_comic_book(title)
    issue_title = get_safe_title(comic_book.get_comic_issue_title())
    print(
        f'Title: "{title:<{max_len}}", {issue_title},'
        f' jpgs: {", ".join(get_abbrev_jpg_page_list(comic_book))}'
    )
