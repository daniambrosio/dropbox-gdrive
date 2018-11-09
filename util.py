#!/usr/bin/python
# encoding=utf8
# -*- coding: utf-8 -*-
import contextlib
import time
import unicodecsv as csv
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')


logger = logging.getLogger("util")

# This function receives a list of dict and writes them to a csv file; if no list of keys is passed the function will use the keys
# stored in the first dict of the list. 
def write_dict_to_csv(csv_filename = "dict.csv", list_dict = [{"no_key","no_value"}], keys = []):
	written_rows = 0
	with stopwatch('print_csv'):
		logger.debug("Writing %s lines into the CSV file: %s", len(list_dict),csv_filename)
		with open(csv_filename, 'w') as csvfile:
			w = csv.DictWriter(csvfile, keys, encoding='utf-8')
			w.writeheader()

			for item in list_dict:
				w.writerow(item)
				written_rows += 1

	return written_rows

# this method will return a list of dicts found comparing the name sith the content of the key
def search(name, key, files):
	logger.debug("searching '%s' value using key '%s'...",name.encode('utf-8'),key)
	return [element for element in files if element[key].encode('utf-8') == name.encode('utf-8')]


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        logger.info('Total elapsed time for %s: %.3f', message, t1 - t0)
    return;


if __name__ == '__main__':
    print "This is just an util module - nothing to do if called in standalone script"