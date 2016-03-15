# -*- coding: utf-8 -*-
import SocketServer
import json

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_clients = {}
history = []

help_text = 'Available requests:\n\
            login <username> - log in with the given username\n\
            logout - log out\n\
            msg <message> - send message\n\
            names - list users in chat\n\
            help - view help text\n'


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    username = ''

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            msg = json.loads(received_string)
            self.handle_msg(msg)

    def handle_msg(self, msg):

        if msg["request"] == "login":
            if msg["content"] in connected_clients.keys():
                self.send_message("The user " + msg["content"] + " is already logged in.")
            else:
                self.username = msg["content"]
                connected_clients[self.username] = self
                self.send_message("Login as " + self.username + " successful.")

        elif msg["request"] == "logout":
            del connected_clients[msg["content"]]
            self.connection.close()

        elif msg["request"] == "msg":
            self.send_message(msg["content"])

        elif msg["request"] == "names":
            usernames = ''.join(connected_clients.keys())
            self.send_message(usernames)

        elif msg["request"] == "help":
            usernames = ''.join(connected_clients.keys())
            self.send_message(usernames)

        else:
            self.send_message("Invalid request.")

    def send_message(self, timestamp, sender, response, content):
        d = {"timestamp": timestamp, "sender": sender, "response": response, "content": content}
        self.connection.send(json.dumps(d))


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