import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QColor, QPalette, QPixmap
from PyQt5.QtCore import Qt

# Colors:
FIELD_COLOR = "#21252b"
FONT_COLOR = "#dcdcdc"
FONT_FAMILY = "Roboto, sans-seri"

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to res
res_path = os.path.join(script_dir, '../..', 'res')



class PlayingField(QWidget):
    def __init__(self):
        super().__init__()

        self.setFocusPolicy(Qt.StrongFocus)
        self.controller = None
        # self.playerMemory = []

        layout = QVBoxLayout()

        image_path = res_path+"/title.png"

        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(450, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setStyleSheet("border: none; padding-top: 20px;")
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label, alignment=Qt.AlignBottom)

        image_path = res_path+"/controls.png"

        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setStyleSheet("border: none; padding-top: 20px;")
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label, alignment=Qt.AlignBottom)

        self.status_label = QLabel("\nWaiting for Players . . .")
        self.status_label.setStyleSheet(
            f"padding-bottom: 20px; font-size: 20px; color: {FONT_COLOR}; font-family: {FONT_FAMILY};")
        layout.addWidget(self.status_label, alignment=Qt.AlignTop)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)
        self.setLayout(layout)

        self.grid_labels = []
        for i in range(6):
            row = []
            for j in range(7):
                label = QLabel()
                label.setMinimumHeight(50)
                label.setAutoFillBackground(True)
                palette = label.palette()
                palette.setColor(QPalette.Background, QColor(FIELD_COLOR))
                label.setPalette(palette)
                row.append(label)
                self.grid_layout.addWidget(label, i, j)
            self.grid_labels.append(row)

    def setController(self, controller):
        self.controller = controller

    def updateStatus(self, message):
        self.status_label.setText(message)

    def keyPressEvent(self, event):
        if self.controller is not None:
            self.controller.keyPressEvent(event)

    def updateBoard(self, board, preview_column):
        #print("Updating PlayingField...")
        self.clear_preview_row()
        self.update_board_cells(board)
        if preview_column is not None:
            self.update_preview_column(preview_column)

    def clear_preview_row(self):
        #print("Clearing preview row...")
        for j in range(7):
            palette = self.grid_labels[0][j].palette()
            palette.setColor(QPalette.Background, QColor(FIELD_COLOR))
            self.grid_labels[0][j].setPalette(palette)

    def clear_win_lable(self):
        self.grid_labels[0][2].setText("")
        self.grid_labels[0][3].setText("")
        self.grid_labels[0][4].setText("")
        self.grid_labels[0][5].setText("")


    def update_board_cells(self, board):
        #print("Updating board cells...")
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if self.grid_labels[i][j].text() == "":
                    color = self.get_color_for_cell(cell)
                    if color is not None:
                        self.update_cell_color(i, j, color)

    def get_color_for_cell(self, cell):
        #print("getting color for cell")
        if cell == 0:  # If the cell is empty
            return FIELD_COLOR
        else:  # If the cell is occupied by a player
            color = self.get_player_color(cell)
            if color is None:
                print(f"No player with ID {cell} found.")
            return color

    def get_player_color(self, playerID):
        player = self.controller.player_manager.find_player_by_id(playerID)
        if player is not None:
            return player.color
        return FIELD_COLOR

    def update_cell_color(self, i, j, color):
        #print("update_cell_color")
        palette = self.grid_labels[i][j].palette()
        palette.setColor(QPalette.Background, QColor(color))
        self.grid_labels[i][j].setPalette(palette)

    def update_preview_column(self, preview_column):
        current_player = self.controller.player_manager.find_player_by_id(self.controller.current_playerID)
        if current_player is not None:
            color = current_player.color
            self.update_cell_color(0, preview_column, color)
        #else:
            #print("No current player found.")
