""" Quick example for testing in folder hierarchy """
from .context import src

import pytest
import threading
import os
import logging
import src.multithread as gb1

class TestThread:
    """ Test suite """

    def setup(self):
        """ setup some modules """
        print("DDD: {}" , os.getcwd())
        if os.path.isfile('logs/testfile.log'):
            os.remove('logs/testfile.log')

    def teardown(self):
        """ teardown once complete """

    def setup_method(self):
        """ per method setup """
        gb1.ZCOUNT = 0

    def teardown_method(self):
        """ per method teardown """
        try:
            gb1.LOCK.release()
        except RuntimeError as excp:
            pass

    def test_run_increase(self):
        # pytest.skip("skipping this test until handle global lock")
        gb1.increase("zzz", 5)
        assert gb1.ZCOUNT == 5

    def test_run_increase_with_negative_value(self):
        # pytest.skip("skipping this test until handle global lock")
        gb1.increase("zzz", -10)
        assert gb1.ZCOUNT == -10

    def test_trigger_event(self):
        tlog = logging.getLogger("test")
        tlog.setLevel(logging.INFO)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('logs/testfile.log')
        tlog.addHandler(f_handler)
        gb1.trigger_event(tlog,  "quicktest", duration=5)
        with open(file="logs/testfile.log", mode="r") as fhxp:
            sl2list = fhxp.readlines()
        assert sl2list[len(sl2list) - 2] == "quicktest: Here is an info tidbit --- at 5 times.\n"