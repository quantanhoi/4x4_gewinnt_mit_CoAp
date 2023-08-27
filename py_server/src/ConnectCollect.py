#ConnectCollect.py

import sys
import threading
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget

from aiocoap import Context, resource
import asyncio

from py_server.src.helperFunctions import read_config_file
from py_server.src.GUI.Leaderboard import Leaderboard
from py_server.src.GameController import GameController
from py_server.src.ControllerResource import ControllerResource

DEBUG_PRINTS = False


class ConnectCollect(QMainWindow):
    def __init__(self):
        super().__init__()

        # ---Basic Initialization---
        self.setObjectName('MainWindow')  # Set the object name
        self.setWindowTitle("Connect-Collect")
        self.setGeometry(150, 100, 800, 800)

        # ---Colors---
        BACKGROUND_COLOR = "#282c34"

        # ---Game Controller & Leaderboard Setup---
        self.game_controller = GameController()
        self.leaderboard = Leaderboard(self.game_controller)
        self.game_controller.setLeaderboard(self.leaderboard)
        self.leaderboard.setFixedWidth(400)  # Set the fixed width

        # ---UI Layout Setup---
        # Create a horizontal layout
        layout = QHBoxLayout()
        # Add the playing field and leaderboard to the layout
        layout.addWidget(self.game_controller.field)
        layout.addWidget(self.leaderboard)
        # Create a container widget to hold the layout
        container = QWidget()
        container.setLayout(layout)
        # Set the container as the central widget
        self.setCentralWidget(container)
        self.setStyleSheet(f"""
            #MainWindow {{ 
                background-color: {BACKGROUND_COLOR};
            }}
        """)
        self.show()

        # ---CoAP Setup---
        self.context = None
        self.loop = None
        self.controller_resource = ControllerResource()
        self.controller_resource.signal_emitter.payload_received.connect(self.handle_payload)
        # Start CoAP server in separate thread
        self.coap_thread = threading.Thread(target=self.start_coap_server, daemon=True)
        self.coap_thread.start()

    #############################################################################################

    async def create_coap_server(self):
        root = resource.Site()
        root.add_resource(('hello',), self.controller_resource)

        ip_address = read_config_file("Server-IP")
        port = 5683

        self.context = await Context.create_server_context(root, bind=(ip_address, port))
        print(f"CoAP server is up and running. Listening on {ip_address}:{port}.")

    def start_coap_server(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self.create_coap_server())
        self.loop.run_forever()

    @pyqtSlot(tuple)
    def handle_payload(self, data):
        client_address, payload = data
        client_ip = client_address.split(':')[0]  # Only keep the IP part

        # Payload: 1-0-01
        isInit = (payload & 0b1000) >> 3
        isHealthCheck = (payload & 0b100) >> 2
        buttonNumber = payload & 0b11  # extract the remaining bits

        if DEBUG_PRINTS:
            print("-------------------------\n"
                  f"client_ip: {client_ip}\n"
                  f"isInit: {isInit}\n"
                  f"isHealthCheck: {isHealthCheck}\n"
                  f"buttonNumber: {buttonNumber}\n"
                  "-------------------------")

        if isInit:
            self.game_controller.addPlayer(client_ip)
            return
        else:
            player = next((p for p in self.game_controller.player_manager.get_players() if p.ip_address == client_ip),
                          None)
            if player:
                player.lastActiveTimestamp = time.time()  # Update the time when client last active
                if not isHealthCheck:
                    currentPlayerID = self.game_controller.current_playerID
                    if player.playerID == currentPlayerID:
                        if buttonNumber == 3:
                            self.game_controller.triggerAction("left")  # left
                        elif buttonNumber == 2:
                            self.game_controller.triggerAction("enter")  # enter
                        elif buttonNumber == 1:
                            self.game_controller.triggerAction("right")  # right
                        else:
                            print("Warning: ControllerInput not listed for game action -->" + str(buttonNumber))
            else:
                print("Error: Player not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnectCollect()
    sys.exit(app.exec_())
