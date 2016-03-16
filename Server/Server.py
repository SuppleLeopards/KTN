# -*- coding: utf-8 -*-
import SocketServer
import json

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        lol.add_thread(self)

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            msg = json.loads(received_string)
            self.handle_msg(msg)

    def handle_msg(self, msg):
        if msg["request"] == "logout":
            self.connection.close()
            #exit()
        self.send_message(msg["content"])

    def send_message(self, msg):
        d = dict(timestamp=None, sender=None, response="msg", content=msg)
        lol.send_msg(json.dumps(d), self)

    def send_msg(self, msg, thread):
        if thread != self:
            self.connection.send(msg)

class Threads_Collector_Master_Pitate:
    def __init__(self):
        self.threads = []

    def add_thread(self, thread):
        self.threads.append(thread)

    def remove_thread(self, thread):
        self.threads.remove(thread)

    def send_msg(self, msg, t):
        for thread in self.threads:
            thread.send_msg(msg, t)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    lol = Threads_Collector_Master_Pitate()
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
"""
Må gjøres:
logout ikke korrekt implementert
login ikke implementert
må generellt lage ferdig alle behandlinger av innput samt recieved

må også sørge for at serveren og klienten kan ta i mot mens en bruker skriver inn/ikke skriver inn
=> en bruker skal ikke trenge å skrive noe for hver gang han skal ha en oppdatert chat.

Serveren må kunne lagre navn samt ha en oversikt over alle navn som skal brukes
"""