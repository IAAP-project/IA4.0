# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import socket
import struct

import select
import bitstring
from packet import Packet


class RobotTCPServer:
    def __init__(self, serverAddress, serverPort):
        logging.info("Initiation du serveur TCP..")
        self.address = serverAddress
        self.port = serverPort
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address, self.port))
        self.clients = []

    def listenForConnections(self):
        self.socket.listen(1)
        logging.info("Listening on port " + str(self.port))
        read_list = [self.socket]
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is self.socket:
                client, adresse_client = self.socket.accept()
                read_list.append(client)
                self.clients.append(client)
                logging.info("Connection reçue de", adresse_client)
            else:
                data = s.recv(1024)
                if data:
                    # traitement
                    pass
                else:
                    s.close()
                    read_list.remove(s)

    def sendPacket(self, packet: Packet):
        if self.socket.fileno() == -1:
            logging.info("Connexion fermée. L'envoi ne peut être effectué.")
            return

        for i in range(len(self.clients)):
            self.clients[i].send(packet.stream.bytes)



'''
# test..
if __name__ == '__main__':
    stream = bitstring.BitStream()
    print(bytes.fromhex('ff110000'))
    stream.append(bytes.fromhex('11110000'))
    stream.append(struct.pack('>i', 2))
    stream.overwrite(bytes.fromhex('0000000000'), 24)
    print(int.from_bytes(stream.bytes[0:4], 'big'))
    print(stream.bytes)
'''