# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        '''
        self.connection.bind((host,server_port))

        self.connection.listen(5)
        '''
        self.host = host
        self.server_port = server_port
        
        # TODO: Finish init process with necessary code
        self.d = dict(request=None, content=None)
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        print("Connected to server")

        while(True):
            msg = raw_input("Skriv:")
            self.check_msg(msg)
            self.receive_message(self.connection.recv(4096))


        
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        d = json.loads(message)
        print d["content"]

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(json.dumps(data))
        
    # More methods may be needed!
    def help(self):
        pass

    def check_msg(self, msg):
        i = msg.index(" ")
        req = msg[0:i]
        con = msg[i+1:]
        d = dict(request=req, content=con)
        print d
        self.send_payload(d)
        if req == "logout":
            self.disconnect()


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
