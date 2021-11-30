import threading
import time

from numpy import ndarray

from packet import Packet
from robot_server import RobotTCPServer
import config

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


if __name__ == '__main__':
    serveur = RobotTCPServer(config.ADRESSE, config.PORT)

    serveur_thread = threading.Thread(target=serveur.listenForConnections)
    # Exit the server thread when the main thread terminates
    serveur_thread.daemon = True
    serveur_thread.start()
    print("Réception de connexions par le thread:", serveur_thread.name)
