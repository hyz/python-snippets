#!/usr/bin/env python
#
# http://apple.stackexchange.com/questions/90040/look-up-a-word-in-dictionary-app-in-terminal
#

import sys
from DictionaryServices import *

def main():
    try:
        searchword = sys.argv[1].decode('utf-8')
    except IndexError:
        errmsg = 'You did not enter any terms to look up in the Dictionary.'
        print(errmsg)
        sys.exit()
    wordrange = (0, len(searchword))
    dictresult = DCSCopyTextDefinition(None, searchword, wordrange)
    if dictresult:
        print(dictresult.encode('utf-8'))
    else:
        errmsg = "'%s' not found in Dictionary." % (searchword)
        print(errmsg.encode('utf-8'))

if __name__ == '__main__':
    main()

