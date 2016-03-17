# -*- coding: utf-8 -*-
import SocketServer
import json
from time import strftime
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


def getClients():
    return connected_clients

def addClient(username, handler):
    if not username in connected_clients:
        connected_clients[username] = handler
        return True
    else:
        return False

def removeClient(username):
    if username in connected_clients:
        connected_clients.remove(username)
        return True
    else:
        return False
def username_Taken(username):
    if username in connected_clients:
        return True
    return False

def send_message(message, username):
    for key in connected_clients.keys():
        if not key == username:
            connected_clients[key].connection.send(json.dumps(message))


def getHistory():
    return history

def setHistory(dict):
    history.append(dict)


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
        self.username = ""
        self.is_logged_in = False

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            msg = json.loads(received_string)
            self.handle_msg(msg)

    def handle_msg(self, msg):
        print(msg)
        request = msg["request"]
        content = msg["content"]

        if request == "login":
            username = msg["content"]
            if username_Taken(username):
                self.send_local("error", "The username " + username + " is already taken.")
            else:
                self.username = username
                self.is_logged_in = True
                addClient(username, self)
                print(getClients())
                print(self.username)
                self.send_local("info", "Loggin was sucsessfull")
                self.send_message("info", self.username + " logged in")

        elif request == "logout":
            try:
                removeClient(self.username)
            except:
                pass
            self.send_message(self, "Logout successful")
            self.connection.close()

        elif request == "msg":
            if self.is_logged_in:
                self.send_message("msg", content, self.username)
            else:
                self.send_local("error", "You are not logged in")
        elif request == "names":
            usernames = '\n'.join(connected_clients)
            self.send_local("names", usernames)

        #Må endres help skal sende liste over alle funskjoner
        elif msg["request"] == "help":
            usernames = '\n'.join(connected_clients)
            self.send_message(usernames)

        else:
            self.send_local(self.make_dict("error","Message wrong"))

    def send_local(self, response, content, sender="Server"):
        self.connection.send(json.dumps(self.make_dict(response,content,sender)))

    def send_message(self, response, content, sender="Server"):
        d = self.make_dict(response, content, sender)
        #print(d)
        send_message(d, self.username)

    def make_dict(self, response, content, sender="Server"):
        return dict(timestamp=strftime("%H:%M:%S"), sender=sender, response=response, content=content)

    def send_msg(self, msg, thread):
        if thread != self:
            self.connection.send(msg)


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