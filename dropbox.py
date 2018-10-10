import sys

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression


import dropbox

# OAuth2 access token.  TODO: login etc.
TOKEN=""
