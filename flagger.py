from termcolor import colored
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
SUBMIT_INTERVAL = 60 #time in seconds

def updateFlag(flag, state):
    con = mdb.connect(DB_HOST, USER, PASSWORD, DB_NAME)
    cur = con.cursor()
    cur.execute('UPDATE flags SET state="%s" WHERE flag="%s";', (state, flag))
    con.commit()
    con.close()

def extractFlags(state):
    con = mdb.connect(DB_HOST, USER, PASSWORD, DB_NAME)
    cur = con.cursor
    cur.execute('SELECT flag FROM flags WHERE state="%s";', state)
    results = cur.fetchall()
    flaglist = [val for sublist in results for val in sublist]
    con.close()
    return flaglist

def submit_flags(flaglist):
    accepted = 0
    too_old = 0
    own = 0
    already_submitted = 0
    later = 0
    no_such_flag = 0
    services_down = set()
    unknown_error = set()

    print ('Submitting '+str(len(flaglist))+' Flags', 'green')

    session = telnetlib.Telnet(FLAGSERVER, FLAG_PORT, 10)
    #invatigate welcome message!
    answer = session.read_until("\n")	

    for flag in flaglist:
        session.write(flag)
        answer = session.read_until("\n").strip()

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

        else:
            updateFlag(flag, "unknown_error")
            unknown_error.add(answer)

    #print status message after each submission round
    print (str(accepted)+' flags scored', 'green') 
    
    if later > 0:
        print (str(later)+' flags to resubmit', 'orange') 
    
    if too_old > 0:
        print (str(too_old)+ 'flags are to old', 'orange') 
    
    if already_submitted > 0:
        print (str(already_submitted)+' flags already submitted', 'orange')
    
    if own > 0:
        print (str(own)+' flags are youre own', 'red') 

    if no_such_flag > 0:
        print (str(no_such_flag)+' no such flags', 'red')

    for service in services_down:
        print (service+'is down.', 'red')

    if len(unknown_error) > 0:
        print ('Following unknown errors hace occoured:', 'red')
        for error in unknown_error:
            print ('  '+error, 'red')
    
    
def submit():
    start = time.time()
    flaglist = extractFlags("new")
    submit_flags(flaglist)		
    end = time.time()
    if (end - start) < SUBMIT_INTERVAL:
        time.sleep(SUBMIT_INTERVAL - (end - start))
    
	
if __name__ == "__main__":
    while 1:
       submit()
