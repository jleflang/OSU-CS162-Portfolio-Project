# Author: James Leflang
# Date: 06/04/2020
# Description: An implementation of the game Gess.


class PlayerNotValid(Exception):
    """Player object is not found."""
    pass


class Player:
    """A Player object. A simple object for holding a value representing the player.
    Args:
        player (int): The player number.
    """
    def __init__(self, player):
        self._player = player

    # Get Methods
    def get_player(self):
        return self._player


class Board:
    """A Board object. Sets the initial board state and contains methods to manipulate the board
        and can identify who possess a given footprint."""
    def __init__(self):
        self._board = [[0 for _ in range(21)],
                       [0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0, 0],
                       [0, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 0, 2, 0, 2, 0, 2, 2, 2, 0],
                       [0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0, 0],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                       [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                       [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                       [0 for _ in range(21)]]

        self._cols_labels = 'abcdefghijklmnopgrst'

    # Set Method
    def set_tile(self, pos, player):
        """Sets the desired position to the player.
        Args:
            pos (str): The desired position.
            player (int): Player value.
        """
        self._board[int(pos[0])][self._cols_labels.index(pos[0])] = player

    # Get Methods
    def get_tile(self, pos):
        """Get the player at this position.
        Args:
            pos (Any): Position of to examine
        Return:
            int: Player that occupies the cell.
        """
        if pos is int:
            col = pos[0]
            row = pos[1]
        else:
            col = self._cols_labels.index(pos[0])
            row = int(pos[1:])

        player = self._board[row][col]

        return player

    def get_position(self, row, col):
        """Returns the numerical position as a string.
        Args:
            row (int): The row number.
            col (int): The column number.
        Return:
            str: Position as a string.
        """
        col_str = self._cols_labels[col]
        pos = col_str.join(str(row))

        return pos

    def get_col_range(self, flag, col):
        """Get a list of the columns that are available to move in.
        Args:
            flag (int): 0 is East, 1 is West.
            col (str): Column string from position string.
        Return:
            list[str]: Range in the given direction.
        """
        rang = []
        start = self._cols_labels.index(col)

        # Find each column label in the acceptable range
        for offset in range(4):
            if flag is 1:
                rang.append(self._cols_labels[start + offset])
            elif flag is -1:
                rang.append(self._cols_labels[start - offset])

        return rang

    def footprint(self, pos):
        """Gets the footprint of the center position.
        Args:
            pos (str): Position of the center.
        Returns:
            list[list[str]]: 2-D array of the footprint
        """

        square = [['0', '0', '0'],
                  ['0', '0', '0'],
                  ['0', '0', '0']]

        row_pos = int(pos[1:]) + 1
        row_neg = int(pos[1:]) - 1

        col_pos = self._cols_labels.find(pos[0]) + 1
        col_neg = self._cols_labels.find(pos[0]) - 1

        square[0][0] = self._cols_labels[col_neg].join(str(row_neg))
        square[0][1] = pos[0].join(str(row_neg))
        square[0][2] = self._cols_labels[col_pos].join(str(row_neg))

        square[1][0] = self._cols_labels[col_neg].join(str(pos[1:]))
        square[1][1] = pos
        square[1][2] = self._cols_labels[col_pos].join(str(pos[1:]))

        square[2][0] = self._cols_labels[col_neg].join(str(row_pos))
        square[2][1] = pos[0].join(str(row_pos))
        square[2][2] = self._cols_labels[col_pos].join(str(row_pos))

        return square


class GessGame:
    """Class that implements the game of Gess."""
    def __init__(self):
        # Set the initial state
        self._board = Board()

        self._player_list = dict()

        p1 = Player(1)
        p2 = Player(2)

        self._game_states = ['UNFINISHED', 'BLACK_WON', 'WHITE_WON']
        self._current_state = self._game_states[0]

        # Set the player default Rings
        self._player_list[p1.get_player()] = [self._board.footprint("l3")]
        self._player_list[p2.get_player()] = [self._board.footprint("l18")]

        # Set first turn
        self._turn = p1.get_player()

    # Get Methods
    def get_game_state(self):
        """Returns the current game state as a string."""
        return self._current_state

    def _next_turn(self):
        """End a turn and hand a turn to the next player.
        Returns:
            int: Player number.
        """
        if self._turn is 2:
            return self._player_list[1]
        else:
            return self._player_list[2]

    def _update_game_state(self):
        """Update the current game state."""

        # Get the next player
        nex_player = self._next_turn()

        # Check if the current player has made a new ring
        for tile in self._board[1:18][1:18]:
            # If the cell is occupied, ignore
            if self._board.get_tile(tile) is not 0:
                continue

            # Setup the check
            ring = 0
            opp_ring = 0
            check_foot = self._board.footprint(tile)

            # Check to see if a ring is formed
            for check_col in check_foot[:]:
                for check_tile in check_col[:]:
                    if self._board.get_tile(check_tile) is self._turn:
                        ring += 1
                    if self._board.get_tile(check_tile) is nex_player:
                        opp_ring += 1

            if ring == 8:
                self._player_list[self._turn].append(check_foot)

        # If the next player is left without a ring, then the current player has won.
        if self._player_list[nex_player][:] is None:
            if nex_player is 0:
                self._current_state = self._game_states[1]
            else:
                self._current_state = self._game_states[2]

    def resign_game(self):
        """A method for the current player to resign.
        Raises:
            PlayerNotValid: Player is not valid.
        """
        if self._turn == 1:
            self._current_state = self._game_states[2]
        elif self._turn == 2:
            self._current_state = self._game_states[1]
        else:
            raise PlayerNotValid

    def make_move(self, piece_pos, future_pos):
        """Make a move for the current game.
        Args:
            piece_pos (str): Position of the piece that the current player wishes to move.
            future_pos (str): Position to move the piece to.
        Returns:
            bool: True if the move was valid, False if the move was invalid.
        """

        col_destin = future_pos[0].lower()
        col_source = piece_pos[0].lower()

        # This block of checks evaluates the desired turn and establishes the validity of the turn
        # If the game has been won, the turn is invalid
        if self._current_state is (self._game_states[1] or self._game_states[2]):
            return False
        # If the move is Out of Bounds, the turn is invalid
        if ((col_destin or col_source) is ['a', 't']) or \
                ((piece_pos[1:] or future_pos[1:]) is ["0", "20"]):
            return False
        # If the piece that the player has selected is not theirs, the turn is invalid
        if self._board.get_tile(piece_pos) is not self._turn:
            return False

        col_only = None
        direction = 0

        # Set the direction flag
        if col_destin > col_source:
            direction = 1
        elif col_destin < col_source:
            direction = -1
        elif future_pos[1:] is piece_pos[1:]:
            col_only = 1

        # Check whether the destination is a valid move based on direction
        if direction is 0:
            if int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3)):
                return False
        elif direction is -1:
            if (col_destin not in self._board.get_col_range(0, col_source)) & \
                    (int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3))):
                return False
        elif direction is 1:
            if (col_destin not in self._board.get_col_range(1, col_source)) & \
                    (int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3))):
                return False
        elif col_only is 1:
            if (col_destin not in self._board.get_col_range(1, col_source)) | \
               (col_destin not in self._board.get_col_range(0, col_source)):
                return False
        else:
            raise AttributeError

        # Establish the current footprint
        source = self._board.footprint(piece_pos)

        # If the move leaves the current player without a ring, the move is invalid
        if (source in self._player_list[self._turn][:]) & \
                (len(self._player_list[self._turn]) is 0):
            return False

        # Determine there are any pieces making the move invalid
        for row in source[:]:
            for tile in row[:]:
                # If the current current indexed tile is blocked, the turn is invalid
                if self._board.get_tile(tile) is self._turn:
                    return False

        # Create the destination footprint
        destin = self._board.footprint(future_pos)

        for ring in self._player_list[self._next_turn()]:
            if source in destin:
                self._player_list[self._next_turn()].remove(ring)

        # Place the pieces in the destination
        for row in destin[:]:
            for tile in row[:]:
                # Capture tiles in the destination
                if self._board.get_tile(tile) is self._next_turn():
                    self._board.set_tile(tile, self._turn)
                # Set the tile to the current player
                self._board.set_tile(tile, self._turn)

        # Update Game State
        self._update_game_state()

        # Pass the turn
        self._turn = self._next_turn()

        return True
