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


def main(dropbox_filename = 'dropbox.csv', gdrive_filename = 'gdrive.csv', merged_filename = 'merged.csv', delimiter_char = ","):

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
				for result in search_result:
					merge = dropbox_file # copy the dropbox dict, because even if no success in search, the dropbox file should go to merge
					# normally there whill only be ONE result
					merge['search_result_count'] = len(search_result)
					merge['search_result_size_match'] = (result['gdrive_size'] == dropbox_file['dropbox_size'])
					merge.update(result) # add the gdrive data found to the merge, related to the dropbox search
					merged_files.append(merge)
					# logger.debug('Merged element: %s',merge)
					keys = list(set(merge.keys() + keys))

		# Write merged file to csv output
		# sort keys before writing do cask file
		keys = sorted(keys)

		with stopwatch('write_csv'):
			logger.info("writing %s lines from memory into CSV merged file",len(merged_files))
			with open(merged_filename, 'w') as csvfile:
				w = csv.DictWriter(csvfile, keys, encoding='utf-8')
				w.writeheader()

				for item in merged_files:
					w.writerow(item)
		

	return;

# this method will return a list of dicts found comparing the name sith the content of the key
def search(name, key, files):
	logger.debug("searching '%s' value using key '%s'...",name,key)
	return [element for element in files if element[key] == name]


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