#flagSubmitter

Simple flagsubmitter.

Requirements flagger:
  * MySQL
  * MySQL Python
  * termcolor
  * parallel

Use the wrapper only after checking the regex eg via `grep -o '\w\{31\}='`

quick and dirty attackframe work:

Put everything in a while loop and let it run
We need to configure the timeout and parallelisation level of parallel

Put everything in a while loop and let it run
We need ro configure the timeout and parallelisation level og parallel

`cat IP.txt | parallel -j128 --timeout 3 python exploit.py | grep -o '\w\{31\}=' | parallel python wrapper.py SERVICENAME`

Parallel usage:
  * `-j128` Number of parallel threads (128 in this case)
  * `--timeout 3` Timeout for each thread in seconds (3 sec in this case)

Breakdown of the attack framework:
  * `cat IP.txt` write IPs to stdout, best would be to check which services are up in advance via scoreboard
  * `parallel python exploit.py` parallel creates a process for each line it receives from stdin. This value is used as command line argument for the script In this example read the IP in exploit.py via sys.argv[1]. The exploit can write everything to stdout but must write the flag!
  * `grep -o '\w\{31\}='` grep matches the flag soulely outputting it.
  * `parallel python wrapper.py SERVICENAME` per flag written to stdout parallel spawns a process of wrapper.py with the according service name and appends the flag. The wrapper will write the flag to the DB it does not perform any real checks!

If some process will crash (except for the first one) we will just lose some flags but it will proceed.

parallel has powerful timeout capabilities so the exploit developers don't need to take care of this.

Exploits can still contain debug output and everything devs don't need to apply any regex grep will take care of it
