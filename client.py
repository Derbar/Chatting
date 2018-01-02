import sys
import getpass
from socket import *
import json
import signal
import threading
import ssl

HOST = '127.0.0.1'
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST,PORT)
client = socket(AF_INET, SOCK_STREAM)
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#ssl_sock = context.wrap_socket(client)
#ssl_sock.connect(ADDR)

def receiveText():
    while True:
        data = client.recv(BUFSIZE)
        if not data: break
        print (data)

def chatRooms():
    print ("----- Welcome chatrooms! -----")
    print ("-q: Go to top menu")
    threading._start_new_thread(receiveText, ())
    text =""
    while text != "-q" :
        text = raw_input("> ")
        if text != "" and text != "-q":
            data = json.dumps({'type':1,'id':ID, 'text':text})
            client.send(data)

def viewLoginList():
    data = json.dumps({'type':2})
    client.send(data)
    
    viewlist = client.recv(1024)
    print (viewlist)
    return viewlist

def exitProgram():
    data = json.dumps({'type':-1, 'id': ID})
    client.send(data)
    client.close()
    sys.exit()

def loginFail():
    print ("Login fail. Exit program.")
    exitProgram()

def loginSuccess():
    funcs = ["exitProgram", "chatRooms", "viewLoginList"]

    print ("------- Login Success! -------")
    print ("|     0. Exit program        |")
    print ("|     1. Enter chatroom      |")
    print ("|     2. View login list     |")
    print ("------------------------------")
    num = -1
    while(num!="0" and num!="1" and num!="2"):
        num = raw_input("Please Enter number: ")
        if (num!="0" and num!="1" and num !="2"):
            print ("Input number is wrong!")
        i =0
        for func in funcs:
            if (num == str(i)):
                eval(func+"()")
            i = i+1
        num = -1

def login(id, pwd):
    try: 
        client.connect(ADDR)
    except Exception as e:
        print ('Connection error! %s:%s'%ADDR)
        sys.exit()
    
    data = json.dumps({'type':0,'id': id, 'pwd':pwd})
    client.send(data)

    while 1:
        ret = client.recv(BUFSIZE)
        if ret != "":
            break
        print (ret)

    if (ret == "True"):
        return True
    else:
        return False

def main():
    print ("***** Please Login. Contact admin for sign up *****")
    _id = raw_input("Id: ")
    _pwd = getpass.getpass()
    global ID
    ID = _id
    if (login(_id,_pwd)):
        loginSuccess()
    else :
        loginFail()
    

def signal_term_hadler(signal, frame):
    print ("Killed client")
    exitProgram()

if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal_term_hadler)
    signal.signal(signal.SIGTERM, signal_term_hadler)

    main()
