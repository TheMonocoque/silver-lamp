"""
Sample for threading, asyncio, and loguru
"""
# import time
# import sys
import random
import uuid
import threading
import asyncio
from loguru import logger

#------------------------------------------------------------------------------
def trigger_event(tlog, prefix):
    """ Quick event for threading with logging """
    for count in range(600):
        tlog.debug(f"{prefix}: That's it, beautiful logging.")
        tlog.info(f"{prefix}: Here is an info tidbit --- at {count} times.")
        tlog.error(f"{prefix}: Whoa, an error is found here.")
        # time.sleep(1)

#------------------------------------------------------------------------------
async def trigger_event_async(tlog, prefix):
    """ Quick event for threading with logging """
    while True:
        msg_id = str(uuid.uuid4())
        tlog.debug(f"{prefix}: That's it, beautiful logging.")
        tlog.info(f"{prefix}: Here is an info tidbit -------  {msg_id}.")
        tlog.error(f"{prefix}: Whoa, an error is found here.")
        tlog.info(f"{prefix}: ===============================")
        # time.sleep(10)
        await asyncio.sleep(random.random())

#------------------------------------------------------------------------------
def example_threading(tlog):
    """ Use standard threading module """
    thr1 = threading.Thread(target=trigger_event, args=(tlog, 'thread1',) )
    thr2 = threading.Thread(target=trigger_event, args=(tlog, 'thread2',) )

    thr1.start()
    thr2.start()
    tlog.info("Waiting for threads to finish.")
    thr1.join()
    thr2.join()
    tlog.info("Complete.")

#------------------------------------------------------------------------------
def example_asyncio(tlog):
    """ Sample of asyncio """
    # queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    tlog.info("Hi from asyncio")
    try:
        loop.create_task(trigger_event_async(tlog,"async_thread_001"))
        loop.create_task(trigger_event_async(tlog,"async_thread_002"))
        loop.run_forever()
    except KeyboardInterrupt:
        tlog.info("Processing interrupted")
    finally:
        loop.close()
        tlog.info("Successfully shutdown service.")


#==============================================================================
if __name__ == "__main__":
    # logger.add(sys.stdout,
    #            colorize=True,
    #            format="{time:YYYY-MM-DD at HH::mm:ss} | {level} | {message}")
    logger.add("logs/file.log",
        rotation="100 KB", # rotation="1 MB",
        # format="{time:YYYY-MM-DD at HH::mm:ss} | {level} | {message}",
        compression="zip",
        retention=2)

    # example_threading(logger)
    example_asyncio(logger)
