#!/usr/bin/env python

"""
Just a quick simulation of filtering out unwanted extensions
"""

import os
import sys

### helper lib
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/lib"))
from log_helper import logging_factory


def str_to_tuple(ext: str) -> tuple:
    """convert delimited str to tuple"""
    assert isinstance(ext, str)
    # return tuple(ext.strip(",").split(",")) # NB: while quick, no space hurt
    tmp_list = [x.strip() for x in ext.split(",") if x.strip()]
    return tuple(tmp_list)


def test_match(filen: str, ext_tpl: tuple) -> bool:
    """extension check"""
    assert isinstance(filen, str)
    assert isinstance(ext_tpl, tuple)
    return filen.endswith(ext_tpl)


def produce_scan_list(file_list: list[str], non_prog_ext: tuple) -> list[str]:
    """simulate gh extract to only filtered list"""
    assert isinstance(file_list, list)
    assert isinstance(non_prog_ext, tuple)
    rtn_list: list[str] = []
    for x in file_list:
        if not test_match(x, non_prog_ext):
            rtn_list.append(x)
        # else:
        #     """ test exercise to modify existing iter catastrophe """
        #     file_list.remove(x) # NB: if delete iterating the pointer is lost!
    return rtn_list


if __name__ == "__main__":
    logger = logging_factory()

    # sample non-programming filter extension to remove
    filter_ext: str = ".md,.rst,.info,  ,    .txt"  # spaces due to bad editors
    tpl_remove_ext: tuple = str_to_tuple(filter_ext)
    logger.info(f"{tpl_remove_ext=}")

    # create a sample filelist to test against
    testfiles: list[str] = ["test.java", "README.md", "test.c"]
    testfiles.extend(["random.py", "pseudo.h"])
    testfiles.extend(["TESTING.rst", "HELP.info", "smtp_connect.go"])
    testfiles.extend(["file with spaces.json", "big data dump.txt"])

    # get updated programming scan list
    updated_list: list[str] = produce_scan_list(testfiles, tpl_remove_ext)
    logger.info(f"{testfiles=}")
    logger.info(f"{updated_list=}")
    # del updated_list
    # updated_list = []
    try:
        # if for some reason this was not initialized, then this would not work
        if updated_list:
            logger.info("We should run the scan.")
    except NameError as excp:
        logger.error("List was not initialized!")
    # except Exception as excp:  # OR SHOULD THIS FAIL HARD
    #     logger.error(f"Unknown exception caught. f{excp=}")
    logger.info("Complete")
