from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
import numpy as np


class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Your turn: Player 1")
        layout.addWidget(self.label)

        # Initialize game board and current player
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = 1
        self.current_column = 3
        self.blockInput = False
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        # Create grid of buttons
        self.buttons = []

        for i in range(6):
            row = []
            for j in range(7):
                button = QPushButton()
                button.setFixedSize(100, 100)
                button.setProperty("row", i)
                button.setProperty("column", j)
                button.setStyleSheet("background-color: white; border: 1px solid black;")
                row.append(button)
                self.grid_layout.addWidget(button, i, j)
            self.buttons.append(row)

        layout.addLayout(self.grid_layout)
        self.setLayout(layout)
        self.setFocusPolicy(Qt.StrongFocus)

        # Preview chip in the current column
        self.preview_chip()

        #popup
        self.fake_popup = QWidget(self)
        self.fake_popup.hide()

    #-------------------------------------------------------------------------------------------------------
    # Preview the current chip at the top of the board
    def preview_chip(self):
        color = "red" if self.current_player == 1 else "yellow"
        self.buttons[0][self.current_column].setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    # Move the preview chip one column to the left
    def move_preview_chip_left(self):
        if self.current_column > 0:
            self.buttons[0][self.current_column].setStyleSheet("background-color: white; border: 1px solid black;")
            self.current_column -= 1
            self.preview_chip()

    # Move the preview chip one column to the right
    def move_preview_chip_right(self):
        if self.current_column < 6:
            self.buttons[0][self.current_column].setStyleSheet("background-color: white; border: 1px solid black;")
            self.current_column += 1
            self.preview_chip()

    # Confirm the placement of the preview chip on the board
    def confirm_preview_chip(self):
        self.buttons[0][self.current_column].setStyleSheet("background-color: white; border: 1px solid black;")
        valid_move = self.add_piece(self.current_column)

        if valid_move:
            if self.check_win(self.current_player):
                self.label.setText(f"Spieler {self.current_player} hat gewonnen!")  # Announce the winner
                self.show_winner_popup()
            else:
                # Switch to the other player
                self.current_player = 3 - self.current_player
                self.label.setText(f"Spieler {self.current_player} ist dran.")
                self.preview_chip()

    # -------------------------------------------------------------------------------------------------------

    # Add the piece to the board and update the UI
    def add_piece(self, column):
        for row in range(5, -1, -1):
            if self.board[row, column] == 0:
                self.board[row, column] = self.current_player
                self.update_board(row, column)
                return True
        return False

    # Update the board UI with the current player's color
    def update_board(self, row, column):
        color = "red" if self.current_player == 1 else "yellow"
        self.buttons[row][column].setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    # -------------------------------------------------------------------------------------------------------

    # Controller Input
    def triggerAction(self, controllerInput):
        # trigger game event with controllerInput

        if self.fake_popup.isVisible():
            # popup controls
            if controllerInput == "left":
                self.switchPopupSelect("left")
            if controllerInput == "right":
                self.switchPopupSelect("right")

            elif controllerInput == "enter":
                self.confirmPopupSelect()
        else:
            # game controls
            if controllerInput == "left":
                self.move_preview_chip_left()

            elif controllerInput == "enter":
                self.confirm_preview_chip()

            elif controllerInput == "right":
                self.move_preview_chip_right()

    # Keyboard Input
    def keyReleaseEvent(self, event):
        if self.fake_popup.isVisible():
            # popup controls
            if event.key() in [Qt.Key_D, Qt.Key_Right]:
                self.switchPopupSelect("right")
            elif event.key() in [Qt.Key_A, Qt.Key_Left]:
                self.switchPopupSelect("left")
            # Confirm chip placement
            elif event.key() in [Qt.Key_S, Qt.Key_Down]:
                self.confirmPopupSelect()
        else:
            # game controls
            if event.key() in [Qt.Key_A, Qt.Key_Left]:
                self.move_preview_chip_left()
            elif event.key() in [Qt.Key_D, Qt.Key_Right]:
                self.move_preview_chip_right()
            # Confirm chip placement
            elif event.key() in [Qt.Key_S, Qt.Key_Down]:
                self.confirm_preview_chip()

    # -------------------------------------------------------------------------------------------------------

    # Check if the current player has won
    def check_win(self, player):
        # Check horizontal
        for row in range(6):
            for col in range(4):
                if np.all(self.board[row, col:col + 4] == player):
                    return True

        # Check vertical
        for row in range(3):
            for col in range(7):
                if np.all(self.board[row:row + 4, col] == player):
                    return True

        # Check diagonal /
        for row in range(3):
            for col in range(4):
                if np.all(np.diag(self.board[row:row + 4, col:col + 4]) == player):
                    return True

        # Check diagonal \
        for row in range(3, 6):
            for col in range(4):
                if np.all(np.diag(np.fliplr(self.board[row - 3:row + 1, col:col + 4])) == player):
                    return True

        return False

    # Reset the game
    def reset_game(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = 1
        self.current_column = 3
        for i in range(6):
            for j in range(7):
                self.buttons[i][j].setStyleSheet("background-color: white; border: 1px solid black;")
                self.buttons[i][j].setEnabled(True)
        self.label.setText("Spieler 1 ist dran.")
        self.blockInput = False
        self.preview_chip()

    # -------------------------------------------------------------------------------------------------------

    # Show the winner popup with options to play again or go back to the menu
    def show_winner_popup(self):

        self.fake_popup.setGeometry(250, 300, 300, 100)
        self.fake_popup.setStyleSheet("background-color: white; border: 3px solid black;")

        layout = QHBoxLayout()

        # Create "Play again" button
        play_again_button = QLabel("Play again")
        play_again_button.setProperty("button_id", 1)
        play_again_button.setStyleSheet("border: 5px solid lightblue; padding: 5px;")
        play_again_button.setAlignment(Qt.AlignCenter)
        layout.addWidget(play_again_button)

        # Create "Back to Menu" button
        back_to_menu_button = QLabel("Back to Menu")
        back_to_menu_button.setProperty("button_id", 2)
        back_to_menu_button.setStyleSheet("border: transparent; ")
        back_to_menu_button.setAlignment(Qt.AlignCenter)
        layout.addWidget(back_to_menu_button)

        self.fake_popup.setLayout(layout)
        self.fake_popup.setFocusPolicy(Qt.StrongFocus)
        self.fake_popup.show()
        play_again_button.setFocus()

    def confirmPopupSelect(self):
        current_label = self.fake_popup.focusWidget()
        if current_label:
            if current_label.property("button_id") == 1:
                self.reset_game()
                self.fake_popup.hide()
            elif current_label.property("button_id") == 2:
                self.fake_popup.hide()
                self.switch_to_menu_screen()

    def switchPopupSelect(self, direction):
        current_label = self.fake_popup.focusWidget()
        if current_label:
            if current_label.property("button_id") == 1 and direction == "right":
                # remove old indicator
                current_label.setStyleSheet("border: transparent")
                # switch focus to other Button
                self.fake_popup.children()[2].setFocus()
                # set new indicator
                self.fake_popup.children()[2].setStyleSheet("border: 5px solid lightblue; padding: 5px;")
            elif current_label.property("button_id") == 2 and direction == "left":
                current_label.setStyleSheet("border: transparent")
                self.fake_popup.children()[1].setFocus()
                self.fake_popup.children()[1].setStyleSheet("border: 5px solid lightblue; padding: 5px;")

    def switch_to_menu_screen(self):
        self.parent().parent().switch_to_menu_screen()
