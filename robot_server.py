# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import socket
import struct
import time

import select
import bitstring
from packet import Packet


class RobotTCPServer:
    def __init__(self, serverAddress, serverPort):
        logging.info("Initiation du serveur TCP..")
        self.address = serverAddress
        self.port = serverPort
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.address, self.port))
        self.clients = []
        self.read_list = []

    def listenForConnectionsOrData(self, newConnectionCallback, dataReceivedCallback):
        self.socket.listen(1)
        logging.info("Listening on port " + str(self.port))
        self.read_list = [self.socket]
        #readable, writable, errored = select.select(read_list, [], [])
        while True:
            for s in self.read_list:
                if s is self.socket:
                    if len(self.clients) == 0:
                        client, adresse_client = self.socket.accept()
                        self.read_list.append(client)
                        self.clients.append(client)
                        newConnectionCallback(client)
                else:
                    try:
                        data = s.recv(1024)
                        if data:
                            dataReceivedCallback(data)
                        else:
                            self.closeConnection(s)
                    except ConnectionResetError:
                        self.closeConnection(s)

            time.sleep(1)

    def closeConnection(self, s):
        s.close()
        self.read_list.remove(s)
        self.clients.remove(s)

    def sendPacket(self, packet):
        if self.socket.fileno() == -1:
            return

        for i in range(len(self.clients)):
            self.clients[i].send(packet.stream.bytes)

    def disconnect(self):
        for s in self.read_list:
            s.close()



