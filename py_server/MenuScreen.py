from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt


class MenuScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.single_player_button = QLabel("Single Player")
        self.single_player_button.setProperty("button_id", 1)
        self.single_player_button.setStyleSheet("border: 5px solid lightblue; padding: 5px;")
        self.single_player_button.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.single_player_button)

        self.multiplayer_button = QLabel("Multiplayer")
        self.multiplayer_button.setProperty("button_id", 2)
        #self.multiplayer_button.setStyleSheet("border: 5px solid transparent; padding: 5px;")
        self.multiplayer_button.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.multiplayer_button)

        self.setLayout(layout)

        # Set focus policy for the widget
        self.setFocusPolicy(Qt.StrongFocus)

    def showEvent(self, event):
        super().showEvent(event)
        self.single_player_button.setFocus()

    def triggerAction(self, controllerInput):
        # trigger game event with controllerInput
        if controllerInput == "left":
            self.move_focus_left()

        elif controllerInput == "enter":
            self.perform_enter_action()

        elif controllerInput == "right":
            self.move_focus_right()

    def keyPressEvent(self, event):
        current_label = self.focusWidget()
        if event.key() in [Qt.Key_A, Qt.Key_Left]:
            self.move_focus_left()
        elif event.key() in [Qt.Key_D, Qt.Key_Right]:
            self.move_focus_right()
        elif event.key() in [Qt.Key_S, Qt.Key_Down]:
            self.perform_enter_action()

    def move_focus_left(self):
        current_label = self.focusWidget()
        #print(current_label.property("button_id"))
        if current_label.property("button_id") == 2:
            current_label.setStyleSheet("border: transparent")
            self.single_player_button.setFocus()
            self.single_player_button.setStyleSheet("border: 5px solid lightblue; padding: 5px;")

    def move_focus_right(self):
        current_label = self.focusWidget()
        #print(current_label.property("button_id"))
        if current_label.property("button_id") == 1:
            current_label.setStyleSheet("border: transparent")
            self.multiplayer_button.setFocus()
            self.multiplayer_button.setStyleSheet("border: 5px solid lightblue; padding: 5px;")

    def perform_enter_action(self):
        current_label = self.focusWidget()
        if current_label:
            if current_label.property("button_id") == 1:
                print("Single Player Key Pressed")
                self.parent().parent().switch_to_game_screen()
            else:
                print("Multiplayer Key Pressed")
                # Do nothing for now
