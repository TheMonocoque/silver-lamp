#!/usr/bin/env python3

import random
import sys, time
import traceback
from loguru import logger


# =================================================================================================
def example(blob=None):
    rtn = None
    try:
        if blob is None:
            rtn = random.randrange(1, 21)
        else:
            rtn = random.randrange(1, blob + 1)
    except (TypeError, ValueError) as excp:
        logger.error("Failed to provide number as input: {}", str(excp))
    return rtn

# -------------------------------------------------------------------------------------------------
def try_10_times():
    """ try 10 times on example """
    for _ in range(10):
        logger.trace("Example returns {}", example())

# -------------------------------------------------------------------------------------------------
def various_ranges():
    for zinp in ["This is not a number", -1, -5, 0, 2]:
        logger.info("Attempt using: {}", zinp)
        logger.info("Test: {}", example(zinp))

# -------------------------------------------------------------------------------------------------
def continue_til_found():
    while True:
        try:
            with open(file="test.txt", mode="r", encoding="utf-8") as fhxp:
                slines = fhxp.readlines()
            for sline in slines:
                logger.trace("SLINE: {}", sline)
        except FileNotFoundError as excp:
            raise excp
        break

# -------------------------------------------------------------------------------------------------
def continue_til_critical():
    logger.debug("Now to try until a crit roll is hit")
    counts = 0
    failures = 0
    while True:
        counts += 1
        roll = example(20)
        logger.trace("Crit check on roll {}: {}", counts, roll)
        if roll == 1:
            logger.error("Critical failure! Penalty 5 seconds.")
            failures += 1
            time.sleep(5)
        elif roll == 20:
            break
        else:
            time.sleep(1)
    logger.info("Done with exercise after {} rolls, and {} failures", counts, failures)

# =================================================================================================

if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, colorize=True, level="DEBUG")

    try_10_times()

    various_ranges()

    retry_count = 0
    while True:
        try:
            continue_til_found()
            break
        except Exception as excp:
            # traceback.print_exc()
            logger.error("Woops - {}", excp)
            continue
        finally:
            retry_count += 1
            if retry_count == 3:
                logger.error("Too many retries, continue to process other jobs.")
                break
            else:
                logger.warning("Failed and will wait 10 seconds to retry")
                time.sleep(10)

    start_time = time.monotonic()
    continue_til_critical()
    end_time = time.monotonic()

    logger.info("It took {} secs to roll a crit.", end_time - start_time)
