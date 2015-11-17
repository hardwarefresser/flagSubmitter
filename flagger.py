import telnetlib
import time
import MySQLdb as mdb

def updateFlag(flag, state):
	con = mdb.connect("172.17.0.13", "root", "toor", "flagDB")		#open DB
	cur = con.cursor()
	print "willdosomething"
	query="UPDATE flags SET state=\""+state+"\" where flag=\""+flag+"\";"	
	cur.execute(query)
	con.commit()
	con.close()

def extractFlags(state):
	con = mdb.connect("172.17.0.13", "root", "toor", "flagDB")		#connect to DB
	cur = con.cursor()							#create cursor
	query="SELECT flag from flags WHERE state=\""+state+"\";"		#SQl query
	cur.execute(query)							#execute query
	results = cur.fetchall()						#fetch all results
	flaglist = [val for sublist in results for val in sublist]		#flatten list
	con.close()
	return flaglist

def runLikeHell(flaglist):
	print "Will open connection"
	session = telnetlib.Telnet("127.0.0.1", 9999, 999)
	print session.read_until("\n")	
	for flag in flaglist:
		session.write(flag)						#send flag to port
		time.sleep(0.25)						#wait a bit
		answer=session.read_until("\n")					#print message
		print answer
		
		if "Accepted" in answer:
			updateFlag(flag,"scored")

		elif "too old" in answer:
			updateFlag(flag,"expired")

		elif "your own" in answer:
			updateFlag(flag, "own")
		
def main():
	print "hello."
	flaglist=extractFlags("new")
	print flaglist
	runLikeHell(flaglist)		
	
if __name__ == "__main__":
	main()		
