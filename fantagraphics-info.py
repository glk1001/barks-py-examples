import logging
import os.path
import sys
from typing import List

from barks_fantagraphics.comic_book import get_abbrev_jpg_page_list, get_safe_title, ComicBook
from barks_fantagraphics.comics_cmd_args import CmdArgs, CmdArgNames
from barks_fantagraphics.comics_consts import RESTORABLE_PAGE_TYPES
from barks_fantagraphics.comics_utils import get_timestamp, get_max_timestamp, setup_logging


def get_issue_titles(title_list: List[str]) -> List[str]:
    issue_ttls = []
    for ttl in title_list:
        comic = comics_database.get_comic_book(ttl)
        issue_ttls.append(get_safe_title(comic.get_comic_issue_title()))

    return issue_ttls


def is_upscayled(comic: ComicBook) -> bool:
    return all_files_exist(comic.get_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES))


def is_restored(comic: ComicBook) -> bool:
    return all_files_exist(comic.get_srce_restored_story_files(RESTORABLE_PAGE_TYPES))


def has_fixes(comic: ComicBook) -> bool:
    mods = [f[1] for f in comic.get_srce_with_fixes_story_files(RESTORABLE_PAGE_TYPES)]
    if any(mods):
        return True

    mods = [f[1] for f in comic.get_final_srce_upscayled_story_files(RESTORABLE_PAGE_TYPES)]
    return any(mods)


def is_built(comic: ComicBook) -> bool:
    if not is_restored(comic):
        return False

    restored_files = comic.get_srce_restored_story_files(RESTORABLE_PAGE_TYPES)
    max_restored_timestamp = get_max_timestamp(restored_files)
    zip_file = comic.get_dest_comic_zip()
    if not os.path.isfile(zip_file):
        return False
    zip_file_timestamp = get_timestamp(zip_file)

    if zip_file_timestamp < max_restored_timestamp:
        logging.debug(f'Zip file is out of date WRT restored files: "{zip_file}".')
        return False

    series_comic_zip_symlink = comic.get_dest_series_comic_zip_symlink()
    if not os.path.islink(series_comic_zip_symlink):
        return False
    series_comic_zip_symlink_timestamp = get_timestamp(series_comic_zip_symlink)

    if series_comic_zip_symlink_timestamp < zip_file_timestamp:
        logging.debug(f'Series symlink is out of date WRT zip file: "{series_comic_zip_symlink}".')
        return False

    year_comic_zip_symlink = comic.get_dest_year_comic_zip_symlink()
    if not os.path.islink(year_comic_zip_symlink):
        return False
    year_comic_zip_symlink_timestamp = get_timestamp(series_comic_zip_symlink)

    if year_comic_zip_symlink_timestamp < zip_file_timestamp:
        logging.debug(f'Year symlink is out of date WRT zip file: "{year_comic_zip_symlink}".')
        return False

    return True


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

title_flags = dict()
for title, issue_title in zip(titles, issue_titles):
    comic_book = comics_database.get_comic_book(title)

    fixes_flag = "F" if has_fixes(comic_book) else " "
    restored_or_upscayled_flag = get_restored_or_upscayled_flag(comic_book)
    built_flag = "B" if is_built(comic_book) else " "
    page_list = ", ".join(get_abbrev_jpg_page_list(comic_book))

    title_flags[title] = (fixes_flag, restored_or_upscayled_flag, built_flag, page_list)

for title, issue_title in zip(titles, issue_titles):
    fixes_flag = title_flags[title][0]
    restored_or_upscayled_flag = title_flags[title][1]
    built_flag = title_flags[title][2]
    page_list = title_flags[title][3]

    print(
        f'Title: "{title:<{max_title_len}}", {issue_title:<{max_issue_title_len}},'
        f" {fixes_flag} {restored_or_upscayled_flag} {built_flag},"
        f' jpgs: {page_list}'
    )
