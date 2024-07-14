import argparse
import sys
import os
import atexit
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

libdir :str = os.path.realpath(os.path.dirname(__file__) + '/../lib')
logging.info(f"Path to LIB: {libdir}")
sys.path.append(libdir)

from keyz import keyz
from blacklist import reddington


def arg_run(value: str) -> (str, str):
    logger.info(f"Running {__name__}")
    byte_message = value.encode()
    mykey = keyz('job12341234q234124', byte_message)
    asdf = mykey.produce()
    logger.info(f"b64[{mykey.breakdown()}]: {asdf}")
    try:
        logger.info(f"random: {mykey.randomizer()}")
        return mykey.randomizer(), asdf
    except Exception as excp:
        logger.error(f"[{type(excp).__name__}] - Out of luck, we ran out of randoms.", excp)

def basic_test() -> str:
    mykey = keyz('job12341234q234123', b'asdfasdfasdfqwerqwerqwerqwer')
    asdf = mykey.produce()
    logger.info(f"b64[{mykey.breakdown()}]: {asdf}")
    return asdf + "aaa"

def byebye(): # pragma: no cover
    logger.debug("That's all folks")

if __name__ == "__main__": # pragma: no cover
    logger.info("Start in main")
    atexit.register(byebye)
    logger.info(f"Blacklist - {reddington()}")
    #basic_test()
    # arg testing
    parser = argparse.ArgumentParser()
    #parser.add_argument('-d', '--dmp', default=None)
    parser.add_argument('message', nargs='?', type=str,
                        default='Hellothisisalongerstringtoproduceinto')
    args = parser.parse_args()
    #logger.info(f"args.dmp: {args.dmp}")
    logger.info(f"args.message: {args.message}")
    arg_run(args.message)
