from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QGridLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal

FONT_COLOR = "#dcdcdc"
FONT_FAMILY = "Roboto, sans-seri"

import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to res
res_path = os.path.join(script_dir, '../..', 'res')



class Leaderboard(QWidget):
    update_signal = pyqtSignal()
    def __init__(self, gameController):
        super().__init__()

        self.controller = gameController
        self.title = None
        self.grid_layout = None

        layout = QVBoxLayout()

        image_path = res_path+"/leaderboard.png"

        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(370, 300, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.SmoothTransformation)  # Adjust the size as needed

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setStyleSheet("border: none; padding-top: 20px;")
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label, alignment=Qt.AlignBottom)

        self.waringLightOn = False

        # Create a grid layout for framed points and labels
        self.grid_layout = QGridLayout()

        # spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.grid_layout.addItem(spacerItem, 0, 0, 1, 2)  # 2 is the column span, so it will be added to both columns
        self.grid_layout.setColumnStretch(1, 1)  # make column 1 take up the remaining space

        # Set the grid layout for the window
        layout.addLayout(self.grid_layout)

        self.setLayout(layout)

        self.update_signal.connect(self._updateBoard)

        self.updateBoard()

    def updateBoard(self):
        self.update_signal.emit()

    def _updateBoard(self):

        # Clear all widgets from the grid layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().setParent(None)
            else:
                # Remove spacer items
                self.grid_layout.removeItem(item)

        # Sort leaderboard_data by Points
        leaderboard_data = sorted(self.controller.player_manager.get_players(), key=lambda p: p.points, reverse=True)

        max_players = 9  # Set this to the maximum number of players you'll ever have

        # Create labels with the rank and points, and add them to the grid layout
        for i in range(max_players):
            # If there is a player for this rank, show them
            if i < len(leaderboard_data):
                player = leaderboard_data[i]
                playerPoints = player.points

                rank_label = QLabel(f"#{i + 1}")
                rank_label.setStyleSheet(f"font-size: 38px; color: {FONT_COLOR}; font-family: {FONT_FAMILY};")
                self.grid_layout.addWidget(rank_label, i, 0, alignment=Qt.AlignLeft)

                # Create a frame for the points and image
                frame = QFrame()
                frame.setStyleSheet(f"border: 2px solid white; background-color: {player.color};")
                frame_layout = QHBoxLayout(frame)

                points_label = QLabel("  " + str(playerPoints) + " Points             ")
                points_label.setStyleSheet(f"font-size: 35px;  border: none; font-family: {FONT_FAMILY};")
                frame_layout.addWidget(points_label)
                # Load and display the image
                if player.isKeyboard:
                    image_path = res_path+"/keyboard.png"
                else:
                    image_path = res_path+"/controller.png"

                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.SmoothTransformation)  # Adjust the size as needed

                image_label = QLabel()
                image_label.setPixmap(pixmap)
                image_label.setStyleSheet("border: none;")
                frame_layout.addWidget(image_label, alignment=Qt.AlignRight)

                # Add the frame to the grid layout
                self.grid_layout.addWidget(frame, i, 1, alignment=Qt.AlignLeft)
            else:
                # If there isn't a player for this rank, add a dummy widget
                dummy_widget = QLabel()
                self.grid_layout.addWidget(dummy_widget, i, 0, 1, 2)
