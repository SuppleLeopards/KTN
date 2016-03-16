# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        super(MessageReceiver, self).__init__()
        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection
        self.parser = MessageParser()
        self.start()
    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while True:
            t = self.connection.recv(4096)
            self.client.receive_message(self.parser.parse(t))
