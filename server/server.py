from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person


#Global CONSTANTS

HOST = 'localhost' #locally hosting the server
PORT = 10000
ADDR = (HOST, PORT)  #host-192.168..... port=an integer
BUFSIZ = 512 #how big messages are gonna be 
MAX_CONNECTIONS=10   # max number of clients which can connect to server


SERVER = socket(AF_INET, SOCK_STREAM)  #AF_inet represents IP4 addresses and SOCK_STREAM means use TCP protocol

SERVER.bind(ADDR)   #binds port with server


#Global Var

persons=[] #list to store the list of connected persons

def broadcast(msg,name): #function to display msg to all other person
   
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]", e)

def client_communication(person):
    
    client=person.client
    
    name=client.recv(BUFSIZ).decode("utf8") #ask the name of the client 
    person.set_name(name)
    msg= bytes(f"{name} has joined the chat!", "utf8")  #print client has joined the chat
    broadcast(msg,"")      #broadcasts the message to all other client
    
    while True:
        msg=client.recv(BUFSIZ)     
        
        if msg==bytes("{quit}","utf8"):  #if message by client is quit then close the connection
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
            print(f"[DISCONNECTED] {name} disconnected")
            break
        
        else:
             broadcast(msg, name+": ")
             print(f"{name}: ", msg.decode("utf8"))

def wait_for_connection():
     #server is waiting for connection
    
    while True:
        
        try:
            client,addr=SERVER.accept()     #(host,port) where host is a IpV4 address and port is an integer
            person=Person(addr,client)     #created a new object for person

            persons.append(person)      #adds a new person to the list
            print(f"[CONNECTION]{addr} connected to server at {time.time()}")
            
            Thread(target=client_communication,args=(person,)).start()  #creates a new thread for each connection
        except Exception as e:   
            print("[EXCEPTION]",e)   
            break
    
    print("SERVER STOPPED WORKING")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # SERVER will be listening till 10 connection 
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)  #creates a new thread for function waiting for connection
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()