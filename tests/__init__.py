# TODO implement this workarround to make test discover work
import os
import logging
import sys
sys.path.append('src')
from util import Util           # noqa: E402
# from procurement_bot.util import Util

"""
All tests can receive an OS var (DEBUG_TEST) to determine if logging will be used during tests.
A typical use case can be the debug of tests itself.
"""
if os.environ.get('DEBUG_TEST', False) in ['TRUE', 'True', 'true', '1', 't', 'y', 'yes']:
    loglevel = logging.DEBUG
    # logformat = Util.LOG_FORMAT_DEBUG
    logformat = Util.LOG_FORMAT_FULL
    logging.basicConfig(level=loglevel, format=logformat)
