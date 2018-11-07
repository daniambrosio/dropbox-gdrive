#!/usr/bin/python
# encoding=utf8
import sys
import os
import contextlib
import datetime
import time
import unicodedata
import ConfigParser
import json
import pprint
import csv
reload(sys)
sys.setdefaultencoding('utf8')


if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect



# OAuth2 access token.  TODO: login etc.
def main():
	# auth_flow = DropboxOAuth2FlowNoRedirect("pn25i8wmcbhoyrz", "nvk11k789ifdfbn")

	# authorize_url = auth_flow.start()
	# print "1. Go to: " + authorize_url
	# print "2. Click \"Allow\" (you might have to log in first)."
	# print "3. Copy the authorization code."
	# auth_code = raw_input("Enter the authorization code here: ").strip()

	# try:
	#     oauth_result = auth_flow.finish(auth_code)
	# except Exception, e:
	#     print('Error: %s' % (e,))
	#     return

	# dbx = dropbox.Dropbox(oauth_result.access_token)

	TOKEN = read_token("DROPBOX_TOKEN")
	print "Token: " + TOKEN

	dbx = dropbox.Dropbox(TOKEN)
	print "checking dropbox file list..."
	listing = list_folder(dbx)
	print('Received a TOTAL of %s files from list_folder' % len(listing)) 


	# for field, possible_values in listing.iteritems():
	# 	print field, ": " , possible_values

	with stopwatch('print_csv'):
		# save to csv file
		print "writing file..."
		# print "keys: ", listing[0].keys()
		with open('dropbox.csv', 'w') as csvfile:
			w = csv.DictWriter(csvfile, listing[0].keys())
			# w = csv.DictWriter(sys.stderr, listing[0].keys())
			w.writeheader()

			for item in listing:
				w.writerow(item)

	return;



def read_token(key):
	configParser = ConfigParser.RawConfigParser()   
	configFilePath = r'./dropbox-gdrive.keys'
	configParser.read(configFilePath)

	return configParser.get('TOKENS', key).strip();


def list_folder(dbx, folder='', subfolder=''):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
        	# create the list of results, because of many possible calls with cursor
        	files = 0
        	results = []
        	res = dbx.files_list_folder(path,True,True)
        	results.append(res)
        	while (res.has_more):
        		files += len(res.entries)
       			print('Received +%s files from list_folder(), com total acumulado de %s' % (len(res.entries), files)) 
        		res = dbx.files_list_folder_continue(res.cursor)
        		results.append(res)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        l = [] # list of files
        for res in results:
        	for entry in res.entries:
				d = {} # dict
				d["id"] = entry.id
				d["name"] = entry.name
				d["path_lower"] = entry.path_lower
				d["path_display"] = entry.path_display
				d["property_groups"] = entry.property_groups
				try:
				    d["size"] = entry.size
				except AttributeError:
					d["size"] = 0

				try:
					d["client_modified"] = entry.client_modified
				except AttributeError:
					d["client_modified"] = ""

				try:
					d["server_modified"] = entry.server_modified
				except AttributeError:
					d["server_modified"] = ""

				try:
					d["rev"] = entry.rev
				except AttributeError:
					d["rev"] = ""

				try:
					d["content_hash"] = entry.content_hash
				except AttributeError:
					d["content_hash"] = ""								

				l.append(d)

        return l

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

def dirmore(instance):
    visible = dir(instance)
    visible += [a for a in set(dir(type)).difference(visible)
                if hasattr(instance, a)]
    return sorted(visible)


if __name__ == '__main__':
    main()