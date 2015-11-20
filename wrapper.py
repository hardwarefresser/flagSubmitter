from flagger import insertFlag
from termcolor import colored, cprint
import sys
import re

try:
    if len(sys.argv) < 2:
        #wron usage
        print "Wrong usage!"
        print "wrapper.py <servicename> <flag>"
    elif len(sys.argv) < 3:
        #oops some one forgot to add service
        if re.match("^\w{31}=$", sys.argv[1]):
            insertFlag(sys.argv[1], "unknown")
        else:
            print "Wrong usage!"
            print "wrapper.py <servicename> <flag>"
    else:
        insertFlag(sys.argv[2], sys.argv[1])

except Exception as e:
    cprint (e, 'red')
