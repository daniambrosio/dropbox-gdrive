#!/usr/bin/python
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def main():
	TOKEN = read_token("DROPBOX_TOKEN")
	print "Token: " + TOKEN


	return;



def read_token(key):
	configParser = ConfigParser.RawConfigParser()   
	configFilePath = r'./dropbox-gdrive.keys'
	configParser.read(configFilePath)

	# dropbox_token = configParser.get('TOKENS', key)
	# print dropbox_token

	return configParser.get('TOKENS', key).strip();




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