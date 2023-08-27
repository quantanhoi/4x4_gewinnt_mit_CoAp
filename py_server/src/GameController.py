#GameController.py

import threading
import time

from PyQt5.QtCore import Qt, QTimer

from py_server.src.GameLogic import GameLogic
from py_server.src.GUI.PlayingField import PlayingField
from py_server.src.PlayerManagement.PlayerManager import PlayerManager

FONT_COLOR = "#dcdcdc"


class GameController:
    def __init__(self):

        # Core attributes
        self.logic = GameLogic()
        self.field = PlayingField()
        self.player_manager = PlayerManager()

        # Game state attributes
        self.game_in_progress = True
        self.current_playerID = None
        self.leaderboard = None

        # Set controller and user input handlers
        self.field.setController(self)
        self.field.keyPressEvent = self.keyPressEvent

        # Threads & Background tasks
        self.check_connection_thread = threading.Thread(target=self.check_player_status, daemon=True)
        self.check_connection_thread.start()

        # add initial keyboard Player
        self.addPlayer("keyboard")

        # Initial setup
        self.updateBoard()

    # Initialization & Setup
    def setLeaderboard(self, leaderboard):
        self.leaderboard = leaderboard

    # Player Management
    def addPlayer(self, ip_address):

        addedPlayerID = self.player_manager.add_player(ip_address)

        if self.current_playerID is None:
            self.current_playerID = addedPlayerID

        if len(self.player_manager.get_players()) == 1:
            self.next_turn()
        else:
            self.updateBoard()

    def removePlayer(self, playerID):

        new_current_playerID = None

        if self.current_playerID == playerID:
            new_current_playerID = self.player_manager.currentPlayerAfterRemoval(playerID)

        if self.player_manager.remove_player(playerID):
            if self.current_playerID == playerID:
                self.current_playerID = new_current_playerID
                print(f"Current player ID updated to: {self.current_playerID}")
            self.logic.removePlayer(playerID)
            self.recalculate_remaining_players_points()
            self.updateBoard()

    def check_player_status(self):
        # In its own thread:
        while True:
            time.sleep(5)  # Check every 5 seconds
            inactive_player_id = self.player_manager.check_inactive_player()
            if inactive_player_id is not None:
                self.removePlayer(inactive_player_id)

    # Game Flow & Logic
    def next_turn(self):

        # Collect all player IDs
        player_ids = [player.playerID for player in self.player_manager.get_players()]

        if not player_ids:
            print("No players available for the turn.")
            return

        if len(player_ids) == 1:
            self.current_playerID = player_ids[0]
            return

        if self.current_playerID is None:
            # If it's the first turn of a Round
            self.current_playerID = player_ids[0]
        else:
            current_index = player_ids.index(self.current_playerID)

            # Move to the next player, wrap around if necessary
            self.current_playerID = player_ids[(current_index + 1) % len(player_ids)]

        print(f"Players turn: {self.current_playerID}")

        self.updateBoard()

    def winnerID(self):
        winner_id = max(self.player_manager.get_players(), key=lambda player: player.points).playerID
        return winner_id

    def checkForWin(self):

        if self.game_in_progress and self.logic.board_full():
            self.game_in_progress = False
            self.current_playerID = self.winnerID()
            self.logic.preview_column = 1
            self.show_winner()

    def reset_game(self):
        self.current_playerID = None
        self.logic.reset_game()
        self.field.updateStatus("\nWaiting for Players . . .")
        print("Game reset: waiting for new players...")

    def recalculate_remaining_players_points(self):
        self.player_manager.recalculate_player_points(self.logic)
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
        players = self.player_manager.get_players()
        if players:
            self.current_playerID = players[0].playerID  # Set to the first player
            self.field.updateStatus("\\nYour Turn: Player 1")
            self.logic.reset_game()
            self.player_manager.reset_player_points()  # Reset points using PlayerManager
            self.field.clear_win_lable()
            self.updateBoard()
            self.game_in_progress = True
        else:
            self.reset_game()

    # User Input Handling
    def keyPressEvent(self, event):
        if self.game_in_progress:

            keyboard_player = self.player_manager.find_keyboardPlayer()

            if keyboard_player is not None and keyboard_player.playerID == self.current_playerID:
                # Only accept movement keys if the current player is the keyboard player
                if event.key() in [Qt.Key_A, Qt.Key_Left]:
                    self.logic.move_preview_chip_left()
                elif event.key() in [Qt.Key_D, Qt.Key_Right]:
                    self.logic.move_preview_chip_right()
                elif event.key() in [Qt.Key_S, Qt.Key_Down]:
                    self.confirmAction()

            # Only allow adding a keyboard player if one doesn't already exist
            if event.key() in [Qt.Key_1] and keyboard_player is None:
                self.addPlayer("keyboard")

            # Only allow removing the keyboard player if one exists
            elif event.key() in [Qt.Key_2] and keyboard_player is not None:
                self.removePlayer(keyboard_player.playerID)

            self.updateBoard()

    def triggerAction(self, controllerInput):
        if self.game_in_progress:
            if self.player_manager.get_players():
                if controllerInput == "left":
                    self.logic.move_preview_chip_left()
                if controllerInput == "right":
                    self.logic.move_preview_chip_right()
                if controllerInput == "enter":
                    self.confirmAction()
            self.updateBoard()

    def confirmAction(self):
        self.logic.add_piece(self.current_playerID)
        print(f"GAME: Player {self.current_playerID} did his move!")
        for player in self.player_manager.get_players():
            if player.playerID == self.current_playerID:
                player.points = self.logic.calculate_points(self.current_playerID)
                break

        self.checkForWin()
        if self.game_in_progress:
            self.next_turn()

    # Display & Updates
    def updateBoard(self):

        board, preview_column = self.logic.get_current_state()
        if self.game_in_progress:
            if self.current_playerID is not None:
                self.field.updateStatus("\nYour turn: Player " + str(self.current_playerID))
            else:
                self.field.updateStatus("\nWaiting for Players . . .")
        self.field.updateBoard(board, preview_column)

        if self.leaderboard:
            self.leaderboard.updateBoard()
