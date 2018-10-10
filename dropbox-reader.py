import sys
import ConfigParser

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox

# OAuth2 access token.  TODO: login etc.
def main():
	TOKEN = read_token("DROPBOX_TOKEN")

	print "TOKEN = %s" % TOKEN
	return;



def read_token(key):
	configParser = ConfigParser.RawConfigParser()   
	configFilePath = r'./dropbox-gdrive.keys'
	configParser.read(configFilePath)

	# dropbox_token = configParser.get('TOKENS', key)
	# print dropbox_token

	return configParser.get('TOKENS', key);

main()