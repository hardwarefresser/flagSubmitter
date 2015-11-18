#flagSubmitter

Simple flagsubmitter.

Requierments flagger:
  * MySQL
  * MySQL Python
  * termcolor

use the wrapper only after checking the regex eg via `grep -o '\w\{31\}='`

quick and dirty attackframe work:

Put everything in a while loop and let it run
We need ro configure the timeout and parallelisation level og parallel

`cat IP.txt| parallel python exploit.py | grep -o '\w\{31\}=' | parallel python wrapper.py SERVICENAME`

A good improvement would be if we only attack hosts with services which are up.
