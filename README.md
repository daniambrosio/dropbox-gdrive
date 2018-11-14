# dropbox-gdrive
Compare folders and their files in dropbox and google drive. 
The purpose of these python modules is to call APIs from Dropbox and Google Drive, in order to get a list of files from both services and compare them.

As a matter of fact, it will consider dropbox as the base list and try to find those files in Google Drive.

## Module files
**merge.py** - This module will look in current directory for the csv files (dropbox.csv and gdrive.csv), load them, extract the important data and as a result will create two files cotaining the resulting analysis: *merged.csv* will contain all the files from dropbox that were found in gdrive and *notfound.csv* obsiously will contain the files that were not.

**dropboxreader.py** - This module will connect to dropbox using the provided key and generate the dropbox.csv containing all the files and their data.
This module will look for a file named dropbox-gdrive.keys that should have the following format and the generated dropbox key:
[TOKENS]
DROPBOX_TOKEN = wWERASDFTfAAAAQBm2yRcmKT9Gf-G2CpJZl4xTs-29384saSADF-1YWJQlm5Rv

**gdrivereader.py** - This module will connect to Google Drive after opening a browser for authentication and generate the gdrive.csv containing all the files and their data.


# Setup Dropbox Python
To install the DBX Platform Python SDK, from the Windows command line or a terminal session enter:

pip install dropbox


[Dropbox for Python Documentation | https://dropbox-sdk-python.readthedocs.io/en/latest/]


# Google Drive
https://developers.google.com/drive/api/v3/quickstart/python

Step 1: Turn on the Drive API
Step 2: Install the Google Client Library
Run the following command to install the library using pip:

pip install --upgrade google-api-python-client oauth2client


https://developers.google.com/api-client-library/python/apis/drive/v2

https://developers.google.com/drive/api/v3/quickstart/python

https://developers.google.com/api-client-library/python/

# TOOLS
sudo pip install unicodecsv
