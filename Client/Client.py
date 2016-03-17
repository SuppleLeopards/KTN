# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json
import re

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

        self.host = host
        self.server_port = server_port
        self.connection.connect((self.host, self.server_port))
        self.msgReceiver = MessageReceiver(self, self.connection)
        self.msgParser = MessageParser()
        
        self.run()

    def run(self):
        print("Connected to server\nReady for input:")

        while(True):
            command = raw_input()
            self.check_msg(command)


        
    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
        print message

    def send_payload(self, data):
        self.connection.send(json.dumps(data))

    def check_msg(self, msg):
        req = ""
        con = ""
        msg = self.check_message(msg.strip())
        try:
            i = msg.index(" ")
            req = msg[0:i].lower()
            con = msg[i+1:]
        except:
            req = msg
            con = None
        d = dict(request=req, content=con)
        if req == "login" and not con == None:
            self.send_payload(d)
        elif req == "help":
            d["content"] = None
            self.send_payload(d)
        elif req == "logout":
            self.send_payload(d)
            self.disconnect()
        elif req == "msg" and not con == None:
            self.send_payload(d)
        elif req == "names":
            d["content"] = None
            self.send_payload(d)
        elif req == "history":
            self.send_payload(d)
        else:
            print ("Invalid command")

    def check_message(self, message):
        pattern = "[a-zA-Z0-9.,-_() ]"
        return "".join(re.findall(pattern, message))





if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
