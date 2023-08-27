from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from shared_resources import player_flags, flags_lock, make_random_move

class PlayerControlWindow(QWidget):
    def __init__(self, player_id, emitter, parent=None):
        super(PlayerControlWindow, self).__init__(parent)
        self.player_id = player_id
        self.emitter = emitter
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Display the player ID
        self.label = QLabel(f"Player {self.player_id + 1}", self)

        self.make_move_btn = QPushButton('Make Move', self)
        self.make_move_btn.clicked.connect(self.on_make_move)

        self.delete_btn = QPushButton('Delete', self)
        self.delete_btn.clicked.connect(self.on_delete)

        layout.addWidget(self.label)
        layout.addWidget(self.make_move_btn)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.setWindowTitle(f'Control - Player {self.player_id + 1}')
        self.setFixedWidth(500)  # Set the width to 500 pixels

        self.show()

    def on_make_move(self):
        if player_flags[self.player_id]:
            make_random_move(self.emitter, self.player_id)

    def on_delete(self):
        with flags_lock:
            player_flags[self.player_id] = False
        print(f"Removed Player {self.player_id + 1}")
        self.close()  # Close the control window for this player


