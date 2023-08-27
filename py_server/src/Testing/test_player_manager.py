import unittest

from py_server.src.PlayerManagement.PlayerManager import PlayerManager


class TestPlayerManager(unittest.TestCase):
    def test_add_player(self):
        player_manager = PlayerManager()
        player_id = player_manager.add_player("192.168.1.1")
        self.assertEqual(len(player_manager.players), 1)
        self.assertEqual(player_manager.players[0].playerID, player_id)

    def test_remove_player(self):
        player_manager = PlayerManager()
        player_id1 = player_manager.add_player("192.168.1.1")
        player_id2 = player_manager.add_player("192.168.1.2")

        # Test removing an existing player
        player_manager.remove_player(player_id1)
        self.assertEqual(len(player_manager.players), 1)
        self.assertEqual(player_manager.players[0].playerID, player_id2)

        # Test removing a non-existing player
        player_manager.remove_player(3)  # Should not raise an error
        self.assertEqual(len(player_manager.players), 1)

    def test_find_player_by_id(self):
        player_manager = PlayerManager()
        player_id = player_manager.add_player("192.168.1.1")

        # Test finding an existing player
        found_player = player_manager.find_player_by_id(player_id)
        self.assertIsNotNone(found_player)
        self.assertEqual(found_player.playerID, player_id)

        # Test finding a non-existing player
        not_found_player = player_manager.find_player_by_id(2)
        self.assertIsNone(not_found_player)

    def test_current_player_after_removal(self):
        player_manager = PlayerManager()
        player_id1 = player_manager.add_player("192.168.1.1")
        player_id2 = player_manager.add_player("192.168.1.2")
        player_id3 = player_manager.add_player("192.168.1.3")

        # Test when removing a middle player
        next_player_id = player_manager.currentPlayerAfterRemoval(player_id2)
        self.assertEqual(next_player_id, player_id3)

        # Test when removing the last player (should wrap around)
        next_player_id = player_manager.currentPlayerAfterRemoval(player_id3)
        self.assertEqual(next_player_id, player_id1)

        # Test when removing a non-existing player (should return None)
        next_player_id = player_manager.currentPlayerAfterRemoval(999)
        self.assertEqual(next_player_id, None)

if __name__ == "__main__":
    unittest.main()
