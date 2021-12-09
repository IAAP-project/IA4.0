import socket
import threading
import time

from numpy import ndarray
import numpy as np

import cv2
from packet import Packet
from robot_server import RobotTCPServer
import config
from PIL import Image

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def sendCapturedImage(path, serveur: RobotTCPServer):
    #img = cv2.imread(path)
    #npArray = np.array(img)

    img = Image.open(path)
    npArray = np.array(img)

    #image = Image.fromarray(npArray)
    #image.show()


    imBytes = npArray.tobytes()
    packet = Packet()
    packet.writeInt32(config.PACKET_ID_CAMERA_IMAGE)
    packet.writeInt32(npArray.shape[0])
    packet.writeInt32(npArray.shape[1])
    packet.writeBytes(imBytes)
    packet.finalizePacket()
    serveur.sendPacket(packet)

def onClientConnected(client: socket):
    global sendPhoto
    sendPhoto = True

def onDataReceived(data: bytes):
    global serveur, sendPhoto
    packet = Packet(data)
    if packet.packetId() == config.PACKET_ID_MASQUE_ETAT:
        sendPhoto = True
        mask = packet.readByte()
        if mask == 0:
            print("Pas de problème de masque")
        else:
            print("Masque non porté")

    elif packet.packetId() == config.PACKET_ID_SERVER_DISCONNECT:
        serveur.disconnect()
        exit(1)

def startOrListenForServerInNewThread():
    serveur_thread = threading.Thread(target=serveur.listenForConnectionsOrData, args=(onClientConnected, onDataReceived, ))
    # Exit the server thread when the main thread terminates
    serveur_thread.daemon = True
    serveur_thread.start()

    return serveur_thread

if __name__ == '__main__':
    serveur = RobotTCPServer(config.ADRESSE, config.PORT)
    sendPhoto = False

    serveur_thread = startOrListenForServerInNewThread()
    print("Réception de connexions par le thread: ", serveur_thread.name)

    while True:
        nbrClients = len(serveur.clients)
        if nbrClients > 0:
            if sendPhoto:
                sendCapturedImage("C:\\Users\\bobba\\OneDrive - Centrale Lille\\Bureau\\Asda\\ziko.jpg", serveur)
                sendPhoto = False
        else:
            sendPhoto = False
        time.sleep(1)
