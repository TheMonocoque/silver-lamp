""" Quick example for testing in folder hierarchy """
from .context import src

import pytest
import os
import glob
import logging
from loguru import logger
import src.multithread as gb1

class TestThread:
    """ Test suite """  
    def setup_method(self):
        """ per method setup """
        try:
            for fhxp in glob.glob("logs/testfile*.log"):
                os.unlink(fhxp)
        except PermissionError as excp:
            print("ERROR: removing file - {}", str(excp))
        gb1.ZCOUNT = 0

    def teardown_method(self):
        """ per method teardown """
        try:
            gb1.LOCK.release()
            for fhxp in glob.glob("logs/testfile*.log"):
                os.unlink(fhxp)
        except RuntimeError as excp:
            pass
        except PermissionError as excp:
            print("ERROR: removing file - {}", str(excp))

    # ---------------------------------------------------------------------------------------------
    loop_count = 0
    def gtest_loop(self):
        self.loop_count += 1
        if self.loop_count > 2:
            return False
        return True
    # ---------------------------------------------------------------------------------------------

    def test_run_increase(self):
        gb1.increase("zzz", 5)
        assert gb1.ZCOUNT == 5

    def test_run_increase_with_negative_value(self):
        gb1.increase("zzz", -10)
        assert gb1.ZCOUNT == -10

    def test_trigger_event(self, request):
        logname = "logs/testfile-" + request.node.name + ".log"
        tlog = logging.getLogger("test")
        tlog.setLevel(logging.INFO)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(logname)
        tlog.addHandler(f_handler)
        gb1.trigger_event(tlog,  "quicktest", duration=5)
        with open(file=logname, mode="r") as fhxp:
            sl2list = fhxp.readlines()
        fhxp.close()
        assert sl2list[len(sl2list) - 2] == "quicktest: Here is an info tidbit --- at 5 times.\n"

    @pytest.mark.asyncio
    async def test_trigger_event_async(self, request):
        # pytest.skip("skipping on how to use async")
        logname = "logs/testfile-" + request.node.name + ".log"
        logger.remove() # remove default stderr for one stdout logger
        logger.add(logname, colorize=True, level="INFO") # DEBUG is default
        zlog = logger
        await gb1.trigger_event_async(zlog, "zzz", self.gtest_loop)
        with open(file=logname, mode="r") as fhxp:
            sl2list = fhxp.readlines()
        fhxp.close()
        assert len(sl2list) == 6
