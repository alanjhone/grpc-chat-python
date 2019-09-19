import threading
from Tkinter import *
#from Tkinter import simpledialog
import tkSimpleDialog as simpledialog

import grpc
import time
import sys

import chatServer_pb2 as chat 
import chatServer_pb2_grpc as rpc

address = 'localhost'
port = 50051


class Client:

    def __init__(self, username):
        # the frame to put ui components on
        self.username = username
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        t = threading.Thread(target=self.__listen_for_messages)
        t.start()

    def __listen_for_messages(self):
        for note in self.conn.ChatStream(chat.Empty()):
            print("[{}]: {}".format(note.name, note.message))

    def send_message(self):
        message = None

        while(message != "q"):
            #time.sleep()
            message = str(raw_input(""))

            if message is not '':
                n = chat.Note()
                n.name = self.username
                n.message = message
                #print("S[{}]: {} ".format(n.name, n.message))
                self.conn.SendNote(n)

        sys.exit()

if __name__ == '__main__':

    username = None
    while username is None:
        username = str(raw_input("Informe o nome do usuario: "))
    
    client = Client(username)
    client.send_message()