#!/usr/bin/env python

import logging
from enum import Enum


def logging_factory():
    logger = logging.getLogger(__name__)
    format_string = "%(asctime)s %(levelname)s %(name)s"
    format_string += " %(filename)s:%(funcName)-10s:%(lineno)03d"
    format_string += " %(message)s"
    logging.basicConfig(format=format_string, level=logging.INFO)
    return logger


class MyStatus(Enum):
    CREATED = 0
    QUEUED = 1
    INPROGRESS = 2
    COMPLETED = 3


class Event(Enum):
    BEGIN = "STARTED"
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    ENDED = "FINISHED"
    END = "FINISHED"
    INPROGRESS = "INPROGRESS"
    PROGRESS = "INPROGRESS"
