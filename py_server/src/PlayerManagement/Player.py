# Player_Colors:
import time


class Player:
    def __init__(self, playerID, ipAddress, color):
        self.playerID = playerID
        self.ip_address = ipAddress
        self.color = color
        self.points = 0
        self.lastActiveTimestamp = time.time()
        self.isKeyboard = ipAddress == "keyboard"

        print(f"Player {playerID} created")

    # this function is called when an object is about to be destroyed
    def __del__(self):
        print(f"destroyed Player with ID {self.playerID}")
