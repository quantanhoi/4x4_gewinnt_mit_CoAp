# GameLogic.py

import numpy as np


class GameLogic:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.preview_column = 3

    def reset_game(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.preview_column = 3

    # Board State & Updates
    def get_current_state(self):
        return self.board.tolist(), self.preview_column

    def board_full(self):
        # If there are no zeros on the board (ignoring the first row), it means the board is full
        return not np.any(self.board[1:] == 0)

    # Player Piece Handling
    def add_piece(self, current_playerID):
        for row in range(5, 0, -1):
            if self.board[row, self.preview_column] == 0:
                self.board[
                    row, self.preview_column] = current_playerID  # Use playerID for board representation
                self.preview_column = 3
                return

    # Scoring & Chain Analysis
    def get_horizontal_chains(self):
        return [row.tolist() for row in self.board]

    def get_vertical_chains(self):
        return [col.tolist() for col in self.board.transpose()]

    def get_diagonal_chains(self):
        diags = [self.board[::-1, :].diagonal(i) for i in range(-self.board.shape[0] + 1, self.board.shape[1])]
        diags.extend(self.board.diagonal(i) for i in range(self.board.shape[1] - 1, -self.board.shape[0], -1))
        return [n.tolist() for n in diags]

    def calculate_points(self, current_playerID):
        total_points = 0
        chains = []
        chains.extend(self.get_horizontal_chains())
        chains.extend(self.get_vertical_chains())
        chains.extend(self.get_diagonal_chains())

        for chain in chains:
            points = 0
            count = 0
            for chip in chain:
                if chip == current_playerID:
                    count += 1
                else:
                    if count > 1:
                        points += count * (count - 1)
                    count = 0  # Reset the count after encountering a different color chip

            # Count the points for the last chain if it was left uninterrupted
            if count > 1:
                points += count * (count - 1)

            total_points += points

        return total_points

    def removePlayer(self, PlayerID):
        # Step 1: Remove Player
        # Replace all instances of PlayerID with 0
        self.board[self.board == PlayerID] = 0

        # Step 2: Implement Gravity
        # For each column, we shift all pieces downward
        for col in range(self.board.shape[1]):
            # Flip the column for easier manipulation (to get bottom row first)
            flipped_column = np.flipud(self.board[:, col])

            # Get all the non-zero values (pieces that remain after removal)
            remaining_pieces = flipped_column[flipped_column != 0]

            # Create a new column initialized with zeros
            new_column = np.zeros(self.board.shape[0], dtype=int)

            # Place the remaining pieces at the bottom of the new column
            new_column[:len(remaining_pieces)] = remaining_pieces

            # Replace the original column with the new column with 'gravity' applied
            self.board[:, col] = np.flipud(new_column)  # Don't forget to flip it back

    # Board Movements
    def move_preview_chip_left(self):
        if self.preview_column > 0:
            self.preview_column -= 1

    def move_preview_chip_right(self):
        if self.preview_column < 6:
            self.preview_column += 1
