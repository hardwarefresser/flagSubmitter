import telnetlib
import time
import MySQLdb as mdb

##session = telnetlib.Telnet("127.0.0.1", 9999, 999)
#session.write("flag{324aaaf64e72c3a8da3b4e41b2a8db05dae83ae8}")
#print session.read_until("\n")

def updateFlag(flag, state):
	con = mdb.connect("172.17.0.13", "root", "toor", "flagDB")#open DB
	cur = con.cursor()
	print "willdosomething"
	query="UPDATE flags SET state=\""+state+"\" where flag=\""+flag+"\";"	
	cur.execute(query)
	con.commit()
	con.close()

def extractFlags(state):
	con = mdb.connect("172.17.0.13", "root", "toor", "flagDB")#open DB
	cur = con.cursor()				#create cursor
	query="SELECT flag from flags WHERE state=\""+state+"\";"	#SQl query
	cur.execute(query)	#execute query
	results = cur.fetchall()#fetch all results
	flaglist = [val for sublist in results for val in sublist]#flatten list
	#print flaglist	#print results
	con.close()
	return flaglist

def runLikeHell(flaglist):
	print "Will open connection"
	session = telnetlib.Telnet("127.0.0.1", 9999, 999)
	print session.read_until("\n")	
	for flag in flaglist:
		session.write(flag)		#write session to port
		time.sleep(0.25)		#wait a bit
		answer=session.read_until("\n")	#print message
		print answer
		
		if "Accepted" in answer:
			updateFlag(flag,"scored")

		elif "too old" in answer:
			updateFlag(flag,"expired")

		elif "your own" in answer:
			updateFlag(flag, "own")
		
		

flaglist=extractFlags("new")
print flaglist
runLikeHell(flaglist)		
