from termcolor import colored, cprint
import threading
import telnetlib
import time
import MySQLdb as mdb

DB_HOST = '172.17.0.1'
USER = 'root'
PASSWORD = 'toor'
DB_NAME = 'flagDB'
FLAGSERVER = '127.0.0.1'
FLAG_PORT = 9999
SUBMIT_INTERVAL = 60	#time in seconds
READ_TIMEOUT = 2 	#timeout in sec to wait after flag submit

def updateFlag(flag, state):
    try:
        con = mdb.connect(DB_HOST, USER, PASSWORD, DB_NAME)
        cur = con.cursor()
        cur.execute('UPDATE flags SET state="%s" WHERE flag="%s";' % (state, flag))
        con.commit()
        con.close()
    except Exception as e:
        cprint (e, 'red')

def extractFlags(state):
    try:
        con = mdb.connect(DB_HOST, USER, PASSWORD, DB_NAME)
        cur = con.cursor()
        cur.execute('SELECT flag FROM flags WHERE state="%s";' % state)
        results = cur.fetchall()
        flaglist = [val for sublist in results for val in sublist]
        con.close()
        return flaglist
    except Exception as e:
        cprint (e, 'red')
        return []

def insertFlag(flag, service):
    try:
        con = mdb.connect(DB_HOST, USER, PASSWORD, DB_NAME)
        cur = con.cursor()
        cur.execute('INSERT INTO flags (flag, service, state) VALUES ("%s", "%s", "new");'
                % (flag, service))
        con.commit()
        con.close()
    except Exception as e:
	if e[0] == 1062:
	    cprint ('Flag already exists in DB', 'red')
	else:
	    cprint (e, 'red')


def submit_flags(flaglist):
    accepted = 0
    too_old = 0
    own = 0
    already_submitted = 0
    later = 0
    no_such_flag = 0
    timeout = 0
    services_down = set()
    unknown_error = set()

    cprint ('Submitting '+str(len(flaglist))+' Flags', 'green')

    session = telnetlib.Telnet(FLAGSERVER, FLAG_PORT, 10)
    #invatigate welcome message!
    answer = session.read_until("\n", READ_TIMEOUT)	

    for flag in flaglist:
        try:
            session.write(flag)
            answer = session.read_until("\n", READ_TIMEOUT).strip()

            if "Accepted" in answer:
                accepted +=1
                updateFlag(flag,"accepted")
            
            elif "too old" in answer:
                too_old +=1
                updateFlag(flag,"expired")
            
            elif "your own" in answer:
                own +=1
                updateFlag(flag, "own")
            
            elif "already submitted" in answer:
                already_submitted +=1
                updateFlag(flag, "already_submitted")
            
            elif "try again later" in answer:
                later +=1
            
            elif "no such flag" in answer:
                no_such_flag +=1
                updateFlag(flag, "no_such_flag")

            elif "your appropriate service" in answer:
                #save service name to set
                services_down.add(answer[33:-10])

            elif answer == "":
                timeout +=1

            else:
                updateFlag(flag, "unknown_error")
                unknown_error.add(answer)

        except Exception as e:
            cprint (e, 'red')

    #print status message after each submission round
    cprint ('{} flags scored'.format(accepted), 'green')
        
    if later > 0:
        cprint ('{} flags to resubmit'.format(later), 'yellow') 
        
    if too_old > 0:
        cprint ('{} flags are too old'.format(too_old), 'yellow') 
        
    if already_submitted > 0:
        cprint ('{} flags already submitted'.format(already_submitted), 'yellow')
        
    if own > 0:
        cprint ('{} flags are youre own'.format(own), 'red') 

    if no_such_flag > 0:
        cprint ('{} no such flags'.format(no_such_flag), 'red')

    if timeout > 0:
        cprint ('{} timeout'.format(timeout), 'red')

    for service in services_down:
        cprint (service+'is down.', 'red')

    if len(unknown_error) > 0:
        cprint ('Following unknown errors hace occoured:', 'red')
        for error in unknown_error:
            cprint ('  '+error, 'red')


def submit():
    start = time.time()
    flaglist = extractFlags("new")
    if flaglist:
        submit_flags(flaglist)
    else:
        cprint ('No flags to submit', 'yellow')
    print ""		
    end = time.time()
    if (end - start) < SUBMIT_INTERVAL:
        time.sleep(SUBMIT_INTERVAL - (end - start))
    
	
if __name__ == "__main__":
    while 1:
       submit()
