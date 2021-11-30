"""
Sample for threading, asyncio, and loguru
"""
import sys
import random
import uuid
import logging
import threading
import asyncio
import time
from loguru import logger

#------------------------------------------------------------------------------
def trigger_event(tlog, prefix):
    """ Quick event for threading with logging """
    for count in range(600):
        tlog.debug(f"{prefix}: That's it, beautiful logging.")
        tlog.info(f"{prefix}: Here is an info tidbit --- at {count} times.")
        tlog.error(f"{prefix}: Whoa, an error is found here.")

#------------------------------------------------------------------------------
async def trigger_event_async(tlog, prefix):
    """ Quick event for threading with logging with async """
    while True:
        msg_id = str(uuid.uuid4())
        tlog.debug(f"{prefix}: That's it, beautiful logging.")
        tlog.trace(f"{prefix}: Here is an info tidbit -------  {msg_id}.")
        tlog.error(f"{prefix}: Whoa, an error is found here.")
        # Test without f-string
        tlog.info("%s: legacy %s" % (prefix, msg_id)) # pylint: disable=consider-using-f-string
        increase(prefix, 1)
        tlog.info(f"{prefix}: ===============================")
        await asyncio.sleep(random.random())

#------------------------------------------------------------------------------
def example_threading():
    """ Use standard threading module """
    tlog = logging.getLogger(__name__)
    thr1 = threading.Thread(target=trigger_event, args=(tlog, 'thread1',) )
    thr2 = threading.Thread(target=trigger_event, args=(tlog, 'thread2',) )

    thr1.start()
    thr2.start()
    tlog.info("Waiting for threads to finish.")
    thr1.join()
    thr2.join()
    tlog.info("Complete.")

#------------------------------------------------------------------------------
def example_asyncio():
    """ Sample of asyncio """
    # queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    tlog = logger # relying on loguru logging

    tlog.info("Hi from asyncio")
    try:
        loop.create_task(trigger_event_async(tlog, "async_thread_001"))
        loop.create_task(trigger_event_async(tlog, "async_thread_002"))
        loop.run_forever()
    except KeyboardInterrupt:
        tlog.info("Processing interrupted")
    finally:
        loop.close()
        tlog.info("Successfully shutdown service.")

#------------------------------------------------------------------------------
def increase(pref, byf):
    """ Sample for locking """
    global ZCOUNT # pylint: disable=global-statement
    lock.acquire()
    ZCOUNT += byf
    time.sleep(0.5)
    hash_value = hash(f'This is the measure: {ZCOUNT}')
    print(f'{pref} - counter={ZCOUNT} and hash={hash_value}')
    lock.release()


#==============================================================================
if __name__ == "__main__":

    lock = threading.Lock()
    ZCOUNT = 0
    #--------------------------------------------------------------------------
    # """ LOGURU """
    logger.remove() # remove default stderr for one stdout logger
    logger.add(sys.stdout, colorize=True, level="DEBUG") # DEBUG is default
    # logger.add("logs/file.log",
    #     rotation="100 KB", # rotation="1 MB",
    #     # format="{time:YYYY-MM-DD at HH::mm:ss} | {level} | {message}",
    #     compression="zip",
    #     retention=2)
    #--------------------------------------------------------------------------
    # """ Standard logging """
    slogger = logging.getLogger(__name__)
    slogger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('logs/sfile.log')
    # """ Create formatters and add it to handlers """
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    # """ Add handlers to the logger """
    slogger.addHandler(c_handler)
    slogger.addHandler(f_handler)
    #--------------------------------------------------------------------------

    # Standard thread and logging
    example_threading()

    # Asyncio and loguru
    example_asyncio()
