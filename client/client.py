from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    HOST = "localhost"
    PORT = 10000
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []   #creates a list of message
        receive_thread = Thread(target=self.receive_messages)  #a new thread for recieving messages from server
        receive_thread.start()
        self.send_message(name)    #send name as the first message
        self.lock = Lock()

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCPETION]", e)
                break

    def send_message(self, msg):
        try:
            self.client_socket.send(bytes(msg, "utf8"))     #send message to local server
            if msg == "{quit}":                     #if message is quit then close socket
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):

        messages_copy = self.messages[:]    #create a copy of messages

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []    #clear out the old messages
        self.lock.release()

        return messages_copy   #return list of messages

    def disconnect(self):

        self.send_message("{quit}")  #disconnect the socket