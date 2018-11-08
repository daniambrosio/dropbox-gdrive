#!/usr/bin/python
# encoding=utf8
# -*- coding: utf-8 -*-
import contextlib
import time
import csv
import logging
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def main(csv_filename = "gdrive.csv"):

	logger.info("Run GDrive authentication. Look for the OAuth window on your browser.") 
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()

	drive = GoogleDrive(gauth)

	logger.info("Start reading files from server. It may take some time to get a response from server, depending on how many files you have.") 
	# file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
	# file_list = drive.ListFile({'q': ''}).GetList()

	keys = [] # list
	l = [] # list
	with stopwatch('list_folder'):
		# Auto-iterate through all files that matches this query
		for file_list in drive.ListFile({'q': "mimeType != 'application/vnd.google-apps.folder' and trashed = false", 'maxResults': 2000}):
			logger.info('Received +%s files from Files.list(), com total acumulado de %s',len(file_list), len(l))
			for entry in file_list:
				keys = list(set(entry.keys() + keys))
				l.append(entry)

	logger.info('Received a TOTAL of %s files from Files.list()',len(l)) 

	with stopwatch('print_csv'):
		logger.info("Writing %s lines into the CSV file: %s", len(file_list),csv_filename)
		with open(csv_filename, 'w') as csvfile:
			w = csv.DictWriter(csvfile, keys, encoding='utf-8')
			w.writeheader()

			for item in l:
				w.writerow(item)

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