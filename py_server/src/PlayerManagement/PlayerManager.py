#PlayerManager.py

import threading
import time

from py_server.src.PlayerManagement.Player import Player


class PlayerManager:
    def __init__(self):
        self.players = []
        self.players_lock = threading.Lock()
        self.next_playerID = 1

        self.available_colors = [
            "#4193ee",  # blue
            "#e45459",  # red
            "#e4ee41",  # yellow
            "#6fc477",  # green
            "#d15cdd",  # pink
            "#db8a49",  # orange
            "#9ba5a5",  # grey
            "#22e1f8",  # turquoise
            "#835cdd",  # purple
        ]

    # Player Look-up & Internal Helper Methods
    def get_players(self):

        with self.players_lock:
            #print([player.playerID for player in self.players])
            return self.players[:]

    def _find_player_by_id(self, playerID):  # No lock here
        for player in self.players:
            if player.playerID == playerID:
                #print(f"Found Player with ID {playerID}")
                return player
        return None

    def find_player_by_id(self, playerID):  # Public method that acquires the lock
        with self.players_lock:
            return self._find_player_by_id(playerID)

    def find_keyboardPlayer(self):
        with self.players_lock:
            for player in self.players:
                if player.isKeyboard:
                    # print(f"Found Player with ID {playerID}")
                    return player
            return None

    def currentPlayerAfterRemoval(self, playerID):
        players = self.get_players()
        if len(players) == 1:
            return None
        current_index = next((i for i, player in enumerate(players) if player.playerID == playerID), None)
        if current_index is not None:
            next_index = (current_index + 1) % len(players) if current_index + 1 < len(players) else 0
            return players[next_index].playerID
        return None

    def add_player(self, ip_address):
        with self.players_lock:
            if not self.available_colors:
                print("Maximum Player count reached")
                return None  # Returning None to indicate that the player was not added

            color = self.available_colors.pop(0)
            new_player = Player(self.next_playerID, ip_address, color)
            self.players.append(new_player)
            self.next_playerID += 1  # Increment the next available player ID
            return new_player.playerID

    def remove_player(self, playerID):
        if not self.players:
            print("No Player to remove")
            return False

        with self.players_lock:
            player_to_remove = self._find_player_by_id(playerID)
            if player_to_remove:
                self.available_colors.append(player_to_remove.color)  # Release the color
                self.players.remove(player_to_remove)
                print(f"Player with ID {playerID} was successfully removed.")
                return True
            else:
                print(f"No player with ID {playerID} found.")
                return False

    def reset_player_points(self):
        with self.players_lock:
            for player in self.players:
                player.points = 0
        print("Player points reset.")

    # Player Points & Scoring
    def recalculate_player_points(self, game_logic):
        with self.players_lock:
            for player in self.players:
                player.points = game_logic.calculate_points(player.playerID)
            print("Points recalculated for remaining players.")

    # Player Activity Checks
    def check_inactive_player(self):
        with self.players_lock:
            current_time = time.time()
            for player in self.players:
                if player.ip_address == "keyboard":
                    continue
                if current_time - player.lastActiveTimestamp > 5:
                    print(f"Player {player.playerID} sent no healthcheck for 5 Seconds")
                    return player.playerID
        return None



