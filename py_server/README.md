### Connect Collect - Server

To start the server:
1. `$env:PYTHONPATH += ";Your_Path\4x4_gewinnt"`
2. `py .\py_server\src\ConnectCollect.py`


### Directory Structure and Files:

1. **Main Game Entry Point**:
    - `ConnectCollect.py`: Main application window for the game. Manages the game, leaderboard, and CoAP server interactions.

2. **Player Management**:
    - `Player.py`: Represents individual player objects.
    - `PlayerManager.py`: Contains logic for managing multiple players.

3. **Game Logic**:
    - `GameLogic.py`: Handles core game mechanics, maintaining board state, resetting the game, and handling player moves.
    - `GameController.py`: Manages core game attributes and game state. Main hub linking GameLogic, PlayingField, and PlayerManager.
    - `ControllerResource.py`: Manages CoAP server interactions and relays data between the server and the game.

4. **Helper Functions**:
    - `helperFunctions.py`: Contains utility functions, including reading from a configuration file.

5. **GUI Components**:
    - `PlayingField.py`: Renders the game board in the GUI.
    - `Leaderboard.py`: Implements the leaderboard GUI.

6. **Testing**:
    - `Testing.py`: Main testing script that simulates player actions and provides functionality for initializing players and health checks.
    - `PlayerControlWindow.py`: GUI window for controlling player actions during testing.
    - `test_player_manager.py`: Contains tests for the player manager component.
    - `shared_resources.py`: Contains resources or utilities shared among multiple testing scripts.

### Linkages and Relationships:

- `GameController` is the main control hub, linking `GameLogic`, `PlayingField`, and `PlayerManager`.
- `PlayingField` interacts with `GameController` for UI updates.
- `GameLogic` interacts with `GameBoard` for game state management.
- `PlayerManager` manages individual `Player` objects.
