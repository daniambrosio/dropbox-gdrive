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


# This code needs that dropboxreader.py and gdrivereader.py are run before, so the CSVs files are available 
def merge(dropbox_filename = 'dropbox.csv', gdrive_filename = 'gdrive.csv', merged_filename = 'merged.csv', notfound_filename = "notfound.csv", delimiter_char = ","):

	dropbox_files = [] # list of files
	gdrive_files = [] # list of files
	merged_files = [] # combined list of files

	# Processa o Dropbox
	filename = dropbox_filename
	logger.info("Pocessando arquivo %s" %(filename))
	with stopwatch('process_dropbox'):
		with open(filename, 'rU') as f:
		    reader = csv.reader(f,delimiter=delimiter_char)
		    next(reader, None)  # skip the headers
		    try:
		        for row in reader:
		        	d = {} # dict
		        	# header of dropbox csv should be like this:
		        	# name,client_modified,rev,path_display,path_lower,server_modified,property_groups,content_hash,id,size
		        	d["dropbox_filename"] = row[0]
		        	d["dropbox_id"] = row[8]
		        	d["dropbox_size"] = int(row[9])
		        	d["dropbox_path_lower"] = row[4]
		        	dropbox_files.append(d)
		        	logger.debug("Dropbox file appended: %s",d)

		    except csv.Error as e:
		        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

		logger.info("Linhas no arquivo %s (%4d)" % (filename,len(dropbox_files)))

	# Processa o GDrive
	filename = gdrive_filename
	logger.info("Pocessando arquivo %s" %(filename))
	with stopwatch('process_gdrive'):
		with open(filename, 'rU') as f:
		    reader = csv.reader(f,delimiter=delimiter_char)
		    next(reader, None)  # skip the headers
		    try:
		        for row in reader:
		        	d = {} # dict
		        	# header of gdrive csv should be like this:
		        	# mimeType,lastViewedByMeDate,appDataContents,thumbnailLink,labels,explicitlyTrashed,etag, # 6
		        	# lastModifyingUserName,writersCanShare,id,sharingUser,kind,videoMediaMetadata,lastModifyingUser,title,ownerNames, # 15
		        	# capabilities,sharedWithMeDate,version,parents,exportLinks,shared,copyRequiresWriterPermission,originalFilename, # 23
		        	# description,webContentLink,editable,embedLink,markedViewedByMeDate,fileExtension,modifiedDate,createdDate,properties, # 32
		        	# md5Checksum,iconLink,imageMediaMetadata,owners,alternateLink,copyable,modifiedByMeDate,downloadUrl,userPermission, # 41
		        	# spaces,quotaBytesUsed,headRevisionId,selfLink,fileSize # 46
		        	# 
		        	# however, since the header of the gdrive files is built on-demand (i.e depending on files properties), we should use DictReader here
		        	d["gdrive_filename"] = row[14]
		        	d["gdrive_id"] = row[9]
		        	d["gdrive_size"] = int(row[46]) if row[46] != '' else 0
		        	d["gdrive_md5"] = row[33]
		        	gdrive_files.append(d)
		        	logger.debug("GDrive file appended: %s",d)
		    except csv.Error as e:
		        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

		logger.info("Linhas no arquivo %s (%4d)" % (filename,len(gdrive_files)))

	# use the dropbox list as reference and search for files in gdrive
	filename = merged_filename
	logger.info("analysing and merging both files into %s" %(filename))
	with stopwatch('merge_files'):
		keys = [] # list of keys in merged dict
		not_found = [] # list of dropbox files not found in gdrive
		for dropbox_file in dropbox_files:
			if (dropbox_file['dropbox_size'] == 0):
				# SKIP - it is a folder
				logger.warning("Skipping dropbox element for being a folder (0 bytes size): %s", dropbox_file['dropbox_filename'])
				pass
			else:
				search_result = search(dropbox_file['dropbox_filename'], 'gdrive_filename', gdrive_files)
				if len(search_result) < 1:
					logger.warning("Not found in search (%s)",dropbox_file['dropbox_filename'])
					merge = dropbox_file # copy the dropbox dict, because even if no success in search, the dropbox file should go to merge
					not_found.append(dropbox_file)
				for result in search_result:
					merge = dropbox_file # copy the dropbox dict, because even if no success in search, the dropbox file should go to merge
					# normally there whill only be ONE result
					merge['search_result_count'] = len(search_result)
					merge['search_result_size_match'] = (result['gdrive_size'] == dropbox_file['dropbox_size'])
					merge.update(result) # add the gdrive data found to the merge, related to the dropbox search
					merged_files.append(merge)
					# logger.debug('Merged element: %s',merge)
					keys = list(set(merge.keys() + keys))

		# sort keys before writing do csvfile
		keys = sorted(keys)

		# write to CSV file the merged analysed list
		written_rows = write_dict_to_csv(merged_filename,merged_files,keys)
		if written_rows > 0:
			logger.info("Successfully written %s rows to CSV_FILE: %s", written_rows, csv_filename)

		# write to CSV file the merged analysed list
		written_rows = write_dict_to_csv(notfound_filename,not_found,dropbox_files[0].keys())
		if written_rows > 0:
			logger.info("Successfully written %s rows to CSV_FILE: %s", written_rows, csv_filename)


	return;


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
	merge()