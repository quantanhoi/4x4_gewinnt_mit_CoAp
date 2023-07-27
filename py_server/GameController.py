import threading

from PyQt5.QtCore import Qt, QTimer

from GameLogic import GameLogic
from PlayingField import PlayingField
from Player import *

FONT_COLOR = "#dcdcdc"


class GameController:
    def __init__(self):
        self.leaderboard = None
        self.players = []
        self.players_lock = threading.Lock()

        self.current_playerID = None

        self.check_connection_thread = threading.Thread(target=self.check_player_status, daemon=True)
        self.check_connection_thread.start()

        self.logic = GameLogic()
        self.field = PlayingField()
        self.field.setController(self)

        self.game_in_progress = True

        # Connect user inputs to the appropriate methods
        self.field.keyPressEvent = self.keyPressEvent

        # Update the playing field to show the initial state
        self.updateBoard()

    def start(self):
        self.field.show()

    def setLeaderboard(self, leaderboard):
        self.leaderboard = leaderboard

    def check_player_status(self):
        while True:
            time.sleep(5)  # Check every 5 seconds
            currentTime = time.time()

            with self.players_lock:
                print("Lock acquired in check_player_status")
                for player in self.players[:]:  # Using slicing to create a copy of the list
                    if player.ip_address == "keyboard":
                        continue
                    if currentTime - player.lastActiveTimestamp > 5:
                        print(f"Player {player.playerID} is inactive")
                        self.removePlayer(player.playerID)
                print("Lock released in check_player_status")

    def updateBoard(self):
        print("updateBoard in GameController")
        board, preview_column = self.logic.get_current_state()
        #print(board)  # Add this line to print out the board state
        if self.game_in_progress:
            if self.current_playerID is not None:
                self.field.updateStatus("\nYour turn: Player " + str(self.current_playerID))
            else:
                self.field.updateStatus("\nWaiting for Players . . .")
        self.field.updateBoard(board, preview_column)

        if self.leaderboard:
            self.leaderboard.updateBoard()

    def next_turn(self):
        # Collect all player IDs for easy navigation
        player_ids = [player.playerID for player in self.players]

        if self.current_playerID is None:
            # If it's the first turn, the next player is the first player
            self.current_playerID = player_ids[0]
        else:
            # Find the index of the current player
            current_index = player_ids.index(self.current_playerID)

            # Move to the next player, wrap around if necessary
            self.current_playerID = player_ids[(current_index + 1) % len(player_ids)]

        # Determine if it's a new round
        if self.current_playerID == player_ids[0]:
            print("next_turn: NEW ROUND")

        # Output the current player
        print(f"Players turn: {self.current_playerID}")

        self.updateBoard()

    def winnerID(self):
        winner_id = max(self.players, key=lambda player: player.points).playerID
        return winner_id

    def checkForWin(self):
        if self.game_in_progress and self.logic.board_full():
            self.game_in_progress = False
            self.current_playerID = self.winnerID()
            self.logic.preview_column = 1
            self.show_winner()

    def confirmAction(self):
        self.logic.add_piece(self.current_playerID)
        for player in self.players:
            if player.playerID == self.current_playerID:
                player.points = self.logic.calculate_points(self.current_playerID)
                break

        self.checkForWin()
        if self.game_in_progress:
            self.next_turn()

    def keyPressEvent(self, event):
        with self.players_lock:
            print("Lock acquired in keyPressEvent")
            if self.game_in_progress:
                if self.players:
                    if event.key() in [Qt.Key_A, Qt.Key_Left]:
                        self.logic.move_preview_chip_left()
                    elif event.key() in [Qt.Key_D, Qt.Key_Right]:
                        self.logic.move_preview_chip_right()
                    elif event.key() in [Qt.Key_S, Qt.Key_Down]:
                        self.confirmAction()

                if event.key() in [Qt.Key_1]:
                    self.addPlayer("keyboard", True)

                elif event.key() in [Qt.Key_2]:
                    self.removePlayer(2)

                self.updateBoard()
            print("Lock released in keyPressEvent")

    def triggerAction(self, controllerInput):
        with self.players_lock:
            print("Lock acquired in triggerAction")
            if self.game_in_progress:
                if self.players:
                    if controllerInput == "left":
                        self.logic.move_preview_chip_left()
                    if controllerInput == "right":
                        self.logic.move_preview_chip_right()
                    if controllerInput == "enter":
                        self.confirmAction()

                self.updateBoard()
            print("Lock released in triggerAction")


    def addPlayer(self, ip_address, connected):
        if len(self.players) < 9:
            freeID = next(i for i in range(1, 10) if i not in [player.playerID for player in self.players])

            self.players.append(Player(freeID, ip_address, connected))

            if self.current_playerID is None:
                self.current_playerID = freeID

            if len(self.players) == 1:
                self.next_turn()
            else:
                self.updateBoard()
        else:
            print("Reached max Playercount of 9")

    def removePlayer(self, playerID):
        if not self.players:
            print("No players to remove.")
            return

        print(f"Attempting to remove player with ID: {playerID}")
        player_to_remove = self.find_player_by_id(playerID)

        if player_to_remove is not None:
            self.handle_player_removal(player_to_remove)
            print(f"Player with ID {playerID} was successfully removed.")
            print(f"current Player after removal: {self.current_playerID}")
        else:
            print(f"No player with ID {playerID} found.")

        if self.current_playerID == playerID:
            self.update_current_playerID()


    def find_player_by_id(self, playerID):
        found_player = next((player for player in self.players if player.playerID == playerID), None)
        return found_player

    def handle_player_removal(self, player):
        self.logic.removePlayer(player.playerID)
        self.players.remove(player)
        self.update_current_playerID_after_removal(player.playerID)
        self.recalculate_remaining_players_points()

    def update_current_playerID_after_removal(self, removed_playerID):
        if self.current_playerID == removed_playerID:
            self.update_current_playerID()

    def update_current_playerID(self):
        if self.players:  # if there are still players left
            self.current_playerID = self.players[0].playerID  # Set to ID of first remaining player
        else:  # if all players are removed
            self.current_playerID = None
        print(f"Current player ID updated to: {self.current_playerID}")

    def reset_game(self):
        self.current_playerID = None
        self.logic.reset_game()
        self.field.updateStatus("\nWaiting for Players . . .")
        print("Game reset: waiting for new players...")

    def recalculate_remaining_players_points(self):
        for player in self.players:
            player.points = self.logic.calculate_points(player.playerID)
        print("Points recalculated for remaining players.")
        self.updateBoard()

    def show_winner(self):
        winner_message = "Player " + str(self.winnerID()) + " wins!"
        next_game_message = "Next game starts in 5 seconds..."
        self.field.updateStatus(winner_message + "\n" + next_game_message)
        self.field.grid_labels[0][2].setText("-")
        self.field.grid_labels[0][2].setStyleSheet(f"font-size: 30px; color: {FONT_COLOR};")
        self.field.grid_labels[0][2].setAlignment(Qt.AlignCenter)
        self.field.grid_labels[0][3].setText("W")
        self.field.grid_labels[0][3].setStyleSheet(f"font-size: 30px; color: {FONT_COLOR};")
        self.field.grid_labels[0][3].setAlignment(Qt.AlignCenter)
        self.field.grid_labels[0][4].setText("O")
        self.field.grid_labels[0][4].setStyleSheet(f"font-size: 30px; color: {FONT_COLOR};")
        self.field.grid_labels[0][4].setAlignment(Qt.AlignCenter)
        self.field.grid_labels[0][5].setText("N")
        self.field.grid_labels[0][5].setStyleSheet(f"font-size: 30px; color: {FONT_COLOR};")
        self.field.grid_labels[0][5].setAlignment(Qt.AlignCenter)
        self.updateBoard()
        QTimer.singleShot(5000, self.start_next_game)

    def start_next_game(self):
        if self.players:
            self.current_playerID = self.players[0].playerID
            self.field.updateStatus("\nYour Turn: Player 1")
            self.logic.reset_game()
            self.field.grid_labels[0][2].setText("")
            self.field.grid_labels[0][3].setText("")
            self.field.grid_labels[0][4].setText("")
            self.field.grid_labels[0][5].setText("")
            for player in self.players:
                player.points = 0
            self.updateBoard()
            self.game_in_progress = True
        else:
            self.reset_game()



