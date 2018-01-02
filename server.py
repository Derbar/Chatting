from socket import *
from select import *
import sys
from time import ctime
import json
import MySQLdb
import signal
import SocketServer
import threading

HOST = '127.0.0.1'
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST,PORT)
DBUSER = "root"
DBPWD = "qwer1234"
DBNAME = "sp"
USERLIST = {}
LOGINLIST = []
CONNECTION = {}

def signal_handler(signal, frame):
    print('Server killed!!')

    sys.exit(0)

def mysqlConnect():
    db = MySQLdb.connect(host=HOST, user=DBUSER,passwd=DBPWD,db=DBNAME)
    cur = db.cursor()
    cur.execute("SELECT * FROM tb_member")
    for row in cur.fetchall():
        print row[1] #id
        print row[2] #pwd
    db.close()

def chatrooms(id,text):
    print ("chatting rooms!!")
    data = id +": "+text
    
    for id in LOGINLIST:
        CONNECTION[id].send(data)

    return data

def viewLoginList():
    print ("view login list!!!!")
    ret = ""
    num = 1
    for id in LOGINLIST:
        ret += str(num) + ". "+id +"\n"
        num = num +1
    if (ret == ""):
        ret = "No login user"
    return ret

def login(id,pwd):
    db = MySQLdb.connect(host=HOST, user=DBUSER,passwd=DBPWD,db=DBNAME)
    cur = db.cursor()
    query = "SELECT * FROM tb_member where username='"+id+"' and password=password('"+pwd+"')"
    cur.execute(query)
    db.close()

    if (len(cur.fetchall()) == 0):
        return False
    else :
        if USERLIST.get(id):
            return False
        USERLIST[id] = True
        LOGINLIST.append(id)
        return True
        

def socketConnect(conn, addr_info):
    print ("Connected by "+str(addr_info))
    id = ""
    try: 
	while True:
	    data = conn.recv(BUFSIZE)
	    while not data: 
	        pass
	    print ("Receive data." + data)
	    data = str(data)
	    jData = json.loads(data) 
            if (jData['type'] == -1) :
                id = jData['id']
                USERLIST[id] = False
                LOGINLIST.remove(id)
                del CONNECTION[id]
	    elif (jData['type'] == 0) :
		result = login(jData['id'], jData['pwd'])
                id = jData['id']
		conn.send(str(result))  
                if (result) :
                    CONNECTION[id] = conn
                else  :
		    break
                    conn.close()

	    elif (jData['type'] == 1):
		chatrooms(jData['id'], jData['text'])
	    elif (jData['type'] == 2):
		conn.send(viewLoginList())
                
    except Exception as e:
        print ("Server Error")
        conn.close()
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(ADDR)
    serverSocket.listen(100)
    print ("Connect...........")
    #threading._start_new_thread(socketConnect, (serverSocket,))
    while True:
        #socketConnect(serverSocket)
	conn, addr_info = serverSocket.accept()
	threading._start_new_thread(socketConnect, (conn, addr_info,))
    serverSocket.close()

if __name__ == "__main__":
    main()
