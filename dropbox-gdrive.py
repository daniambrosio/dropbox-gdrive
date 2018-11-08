#!/usr/bin/python
# encoding=utf8
import sys
import os
import contextlib
import datetime
import time
import unicodecsv as csv
import logging
reload(sys)
sys.setdefaultencoding('utf8')


def main():
		

	return;


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        logger.info('Total elapsed time for %s: %.3f', message, t1 - t0)


if __name__ == '__main__':
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	# # create console handler and set level to debug
	streamHandler = logging.StreamHandler()
	streamHandler.setLevel(logging.INFO)
	# # create formatter
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	# # add formatter to ch
	streamHandler.setFormatter(formatter)

	# # add handler to logger
	logger.addHandler(streamHandler)

	
	# calls the main function
	main()