#!/usr/bin/python
# encoding=utf8
# -*- coding: utf-8 -*-
import contextlib
import time
import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def main():

	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()

	drive = GoogleDrive(gauth)

	print "Start reading files. It may take some time to get a response from server..."
	# Auto-iterate through all files that matches this query
	# file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
	# file_list = drive.ListFile({'q': ''}).GetList()

	keys = [] # list
	l = [] # list
	with stopwatch('list_folder'):
		for file_list in drive.ListFile({'q': "mimeType != 'application/vnd.google-apps.folder' and trashed = false", 'maxResults': 2000}):
			print('Received +%s files from Files.list(), com total acumulado de %s' % (len(file_list), len(l))) 
			for entry in file_list:
				keys = list(set(entry.keys() + keys))
				l.append(entry)

	print('Received a TOTAL of %s files from Files.list()' % len(l)) 

	with stopwatch('print_csv'):
		print "writing file..."
		# print "keys: ", listing[0].keys()
		with open('gdrive.csv', 'w') as csvfile:
			w = csv.DictWriter(csvfile, keys)
			# w = csv.DictWriter(sys.stderr, listing[0].keys())
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
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


if __name__ == '__main__':
    main()