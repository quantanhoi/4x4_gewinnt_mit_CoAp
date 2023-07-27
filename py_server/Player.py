# Player_Colors:
import time

PLAYER_1_COLOR = "#4193ee"  # blue
PLAYER_2_COLOR = "#e45459"  # red
PLAYER_3_COLOR = "#e4ee41"  # yellow
PLAYER_4_COLOR = "#6fc477"  # green
PLAYER_5_COLOR = "#d15cdd"  # pink
PLAYER_6_COLOR = "#db8a49"  # orange
PLAYER_7_COLOR = "#9ba5a5"  # grey
PLAYER_8_COLOR = "#22e1f8"  # turquoise
PLAYER_9_COLOR = "#835cdd"  # purple


class Player:

    colors = [PLAYER_1_COLOR, PLAYER_2_COLOR, PLAYER_3_COLOR, PLAYER_4_COLOR, PLAYER_5_COLOR, PLAYER_6_COLOR,
              PLAYER_7_COLOR, PLAYER_8_COLOR, PLAYER_9_COLOR]

    def __init__(self, id, ip_address, connected):

        self.playerID = id
        self.color = Player.colors[id-1]

        self.ip_address = ip_address

        self.isKeyboard = False
        if ip_address == "keyboard":
            self.isKeyboard = True

        self.controllerConnected = connected

        self.points = 0

        self.lastActiveTimestamp = time.time()  # Initialize timestamp at creation time

        print(f"created Player with ID {self.playerID}")

    # this function is called when an object is about to be destroyed
    def __del__(self):
        print(f"destroyed Player with ID {self.playerID}")


