#!/usr/bin/python
# encoding=utf8
# -*- coding: utf-8 -*-
import sys
import os
import ConfigParser
import json
import logging
import dropbox
from util import *
from dropbox import DropboxOAuth2FlowNoRedirect
reload(sys)
sys.setdefaultencoding('utf8')


# this method will run calling Dropbox to get a list of files and return list of dict containing all the file information retrieved
def dropboxreader():
	# Will read the Dropbox token from a configuration file
	TOKEN = read_token("DROPBOX_TOKEN")

	dbx = dropbox.Dropbox(TOKEN)
	logger.info("Start reading files from server. It may take some time to get a response from server, depending on how many files you have.") 
	listing = list_folder(dbx)
	logger.info('Received a TOTAL of %s files from list_folder' % len(listing)) 

	return listing


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
       			logger.info('Received +%s files from list_folder(), adding to a total of %s',len(res.entries), files)
        		res = dbx.files_list_folder_continue(res.cursor)
        		results.append(res)
    except dropbox.exceptions.ApiError as err:
        logger.critical('Folder listing failed for', path, '-- assumed empty:', err)
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

# this main method will get the files information from GDrive and save them on a CSV file
if __name__ == '__main__':
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)

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
	listing = dropboxreader()

	csv_filename = "dropbox.csv"
	written_rows = write_dict_to_csv(csv_filename,listing,listing[0].keys())
	if written_rows > 0:
		logger.info("Successfully written %s rows to CSV_FILE: %s", written_rows, csv_filename)

