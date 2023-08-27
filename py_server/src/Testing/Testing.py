
from PyQt5.QtWidgets import QApplication
import sys
import time
import threading


from py_server.src.ConnectCollect import ConnectCollect
import faulthandler

from py_server.src.Testing.PlayerControlWindow import PlayerControlWindow

faulthandler.enable()
# In both modules

from shared_resources import player_flags, flags_lock, simulate_payload, TestSignalEmitter, make_random_move

INITIAL_PLAYER_COUNT = 5
ACTION_INIT = 0b1000
ACTION_HEALTH_CHECK = 0b0100

player_control_windows = []  # Store references to player control windows

def init(p_emitter):
    for i in range(INITIAL_PLAYER_COUNT):
        simulate_payload(p_emitter, i + 1, ACTION_INIT)
        control_window = PlayerControlWindow(i, p_emitter)
        player_control_windows.append(control_window)
        time.sleep(0.5)

def healthCheck(emitter):
    global player_flags
    time.sleep(1)
    while True:
        # print(player_flags)
        for player in range(len(player_flags)):
            with flags_lock:  # Acquire the lock
                if player_flags[player]:
                    # Simulate health check for the player if the flag is true
                    simulate_payload(emitter, player + 1, ACTION_HEALTH_CHECK)
        time.sleep(1)  # Adjust the frequency of health checks as needed

def endlessGameSimulation(emitter):
    ROUND = 1

    while True:
        print(f"---ROUND {ROUND}---")
        for player in range(len(player_flags)):
            make_random_move(emitter, player)
        ROUND += 1


if __name__ == "__main__":
    print("START OF DYNAMIC SIMULATION")
    app = QApplication(sys.argv)
    connect_collect = ConnectCollect()

    # Create an instance of the custom signal emitter
    emitter = TestSignalEmitter()

    # Connect the custom signal to the handle_payload method
    emitter.payload_received.connect(connect_collect.handle_payload)

    # Show the ConnectCollect window
    connect_collect.show()

    # Initialize players and their control windows
    init(emitter)

    # Start the healthCheck in a separate thread
    healthCheck_thread = threading.Thread(target=healthCheck, args=(emitter,))
    healthCheck_thread.start()

    endlessGameSimulation = threading.Thread(target=endlessGameSimulation, args=(emitter,))
    endlessGameSimulation.start()

    sys.exit(app.exec_())


