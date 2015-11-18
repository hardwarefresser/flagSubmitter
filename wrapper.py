from flagger import insertFlag
import sys

try:
    insertFlag(sys.argv[2], sys.argv[1])
except Exception as e:
    cprint (e, 'red')
