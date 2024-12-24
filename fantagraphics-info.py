import logging
import os.path
import sys
from typing import List

from barks_fantagraphics.comic_book import get_abbrev_jpg_page_list, get_safe_title, ComicBook
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_utils import setup_logging


def get_issue_titles(title_list: List[str]) -> List[str]:
    issue_ttls = []
    for ttl in title_list:
        comic = comics_database.get_comic_book(ttl)
        issue_ttls.append(get_safe_title(comic.get_comic_issue_title()))

    return issue_ttls


def is_upscayled(comic: ComicBook):
    return all_files_exist(comic.get_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES))


def is_restored(comic: ComicBook):
    return all_files_exist(comic.get_srce_restored_story_files(RESTORABLE_PAGE_TYPES))


def has_fixes(comic: ComicBook):
    mods = [f[1] for f in comic.get_srce_with_fixes_story_files(RESTORABLE_PAGE_TYPES)]
    if any(mods):
        return True

    mods = [f[1] for f in comic.get_final_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES)]
    return any(mods)


def all_files_exist(file_list: List[str]) -> bool:
    for file in file_list:
        if not os.path.isfile(file):
            return False
    return True


def get_restored_or_upscayled_flag(comic: ComicBook) -> str:
    flag = " "
    if is_restored(comic_book):
        flag = "R"
    elif is_upscayled(comic_book):
        flag = "U"
    return flag

cmd_args = CmdArgs("Fantagraphics info", CmdArgNames.VOLUME)
args_ok, error_msg = cmd_args.args_are_valid()
if not args_ok:
    logging.error(error_msg)
    sys.exit(1)

setup_logging(cmd_args.get_log_level())

comics_database = cmd_args.get_comics_database()

titles = cmd_args.get_titles()
max_title_len = max([len(title) for title in titles])

issue_titles = get_issue_titles(titles)
max_issue_title_len = max([len(issue_title) for issue_title in issue_titles])

for title, issue_title in zip(titles, issue_titles):
    comic_book = comics_database.get_comic_book(title)

    fixes_flag = "F" if has_fixes(comic_book) else " "

    print(
        f'Title: "{title:<{max_title_len}}", {issue_title:<{max_issue_title_len}},'
        f" {fixes_flag} {get_restored_or_upscayled_flag(comic_book)},"
        f' jpgs: {", ".join(get_abbrev_jpg_page_list(comic_book))}'
    )
