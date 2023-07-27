import sys
import threading
import time

# ConnectFour.py

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from aiocoap import Context
import asyncio

from Leaderboard import *
from GameController import *
from ControllerResource import *


class ConnectFour(QMainWindow):
    def __init__(self):
        super().__init__()

        # ---- Player Map ---
        # self.player_map = {}
        # self.check_connection_thread = threading.Thread(target=self.check_connections, daemon=True)
        # self.check_connection_thread.start()

        # Colors
        BACKGROUND_COLOR = "#282c34"

        # ---UI---
        self.setObjectName('MainWindow')  # Set the object name
        self.setWindowTitle("Connect-Collect")
        self.setGeometry(150, 100, 800, 800)

        self.game_controller = GameController()
        self.leaderboard = Leaderboard(self.game_controller)
        self.game_controller.setLeaderboard(self.leaderboard)
        self.leaderboard.setFixedWidth(400)  # Set the fixed width

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

        # ---CoAP---
        self.context = None
        self.loop = None

        self.controller_resource = ControllerResource()
        self.controller_resource.signal_emitter.payload_received.connect(self.handle_payload)

        # Start CoAP server in separate thread
        self.coap_thread = threading.Thread(target=self.start_coap_server, daemon=True)
        self.coap_thread.start()

    #############################################################################################

    def check_connections(self):
        while True:
            # Wait for 15 seconds
            time.sleep(15)

            all_connected = True
            # Check all players in the map
            for ip_address, player_info in self.player_map.items():
                if player_info["isConnected"] == 0:
                    all_connected = False
                    print("Player " + str(player_info["playerID"]) + " is not connected")
                    # ToDo: self.gamecontroller.removePlayer(player_id)

            if all_connected:
                # If all players are connected, set all isConnected values to 0
                for ip_address in self.player_map:
                    self.player_map[ip_address]["isConnected"] = 0
                print("all players are connected")
            else:
                # insert what you want to do when the player is not connected here
                print("at least one player is not connected")

    # ---CoAP---------------------------------------------------
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
        isControllerConnected = (payload & 0b1000) >> 3  # extract the first bit
        isHealthCheck = (payload & 0b100) >> 2
        number = payload & 0b11  # extract the remaining bits
        isInit = (payload & 0b10000) >> 4

        print("-------------------------")
        print(f"client_ip: {client_ip}")
        print(f"isControllerConnected: {isControllerConnected}")
        print(f"isHealthCheck: {isHealthCheck}")
        print(f"number: {number}")
        print(f"isInit: {isInit}")
        print("-------------------------")
        print("Lock acquired in handle_payload")
        self.game_controller.players_lock.acquire()
        player = next((p for p in self.game_controller.players if p.ip_address == client_ip), None)
        self.game_controller.players_lock.release()
        print("Lock released in handle_payload")

        if isInit:
            print("init message")
            if not player:
                print("Lock acquired in handle_payload")
                self.game_controller.players_lock.acquire()
                self.game_controller.addPlayer(client_ip, True)
                self.game_controller.players_lock.release()
                print(f"Added new player with IP address {client_ip}")
                print("Lock released in handle_payload")
            else:
                player.isControllerConnected = bool(isControllerConnected)
                print(
                    f"Player with IP address {client_ip} already exists and isControllerConnected status is now {player.controllerConnected}")
            return

        if player:
            if isHealthCheck == 1:
                player.lastActiveTimestamp = time.time()  # Update the time when client last active
                player.isControllerConnected = bool(isControllerConnected)
            else:
                player.lastActiveTimestamp = time.time() if player.controllerConnected else player.lastActiveTimestamp  # Update the time when client last active if controller is connected
                #print("passed timestamp")
                player.isControllerConnected = True
                currentPlayerID = self.game_controller.current_playerID
                print("current_player_index = " + str(currentPlayerID))
                print("own ID = " + str(player.playerID))
                if player.playerID == currentPlayerID:
                    if number == 3:
                        self.game_controller.triggerAction("left")  # left
                    elif number == 0:
                        self.game_controller.triggerAction("enter")  # enter
                    elif number == 1:
                        self.game_controller.triggerAction("right")  # right
                    else:
                        print("Warning: ControllerInput not listed for game action -->" + str(number))




def read_config_file(whatIneed):
    with open('../config.txt', 'r') as file:  # replace with your file path
        for line in file:
            if line.startswith('#'):  # skip comment lines
                continue
            if '=' in line:
                key, value = line.strip().split('=')
                if key == whatIneed:
                    return value

    print(f"Unable to find value for {whatIneed}")
    return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnectFour()
    sys.exit(app.exec_())
