# shared_resources.py
import time

from PyQt5.QtCore import pyqtSignal, QObject
import random
import threading

INITIAL_PLAYER_COUNT = 5
player_flags = [True] * INITIAL_PLAYER_COUNT
flags_lock = threading.Lock()  # Create a lock

class TestSignalEmitter(QObject):
    # Define a custom signal that takes a tuple as an argument
    payload_received = pyqtSignal(tuple)


def simulate_payload(p_emitter, client_ip, payload):
    # Simulate incoming payload by emitting the custom signal
    data = (f'TestController{client_ip}', payload)
    p_emitter.payload_received.emit(data)

def make_random_move(emitter, player):
    # Determine a random number of "left" or "right" actions (0 to 3 times)
    num_actions = random.randint(0, 3)
    action = random.choice([0b0001, 0b0011])  # "left" or "right"

    # Perform the "left" or "right" actions
    for _ in range(num_actions):
        simulate_payload(emitter, player + 1, action)
        time.sleep(0.2)  # Realistic delay for performing actions

    # Perform the "down" action to end the move
    simulate_payload(emitter, player + 1, 0b0010)
    print(f"TEST: PLAYER {player + 1} sent his action to the GAME!")
    time.sleep(0.2)  # Realistic delay for performing actions
