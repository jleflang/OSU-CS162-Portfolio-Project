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
                       [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                       [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                       [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0],
                       [0 for _ in range(21)],
                       [0 for _ in range(21)],
                       [0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0, 0],
                       [0, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 0, 2, 0, 2, 0, 2, 2, 2, 0],
                       [0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 0, 0],
                       [0 for _ in range(21)]]

        self._cols_labels = 'abcdefghijklmnopgrst'

    # Set Method
    def set_tile(self, pos, player):
        """Sets the desired position to the player.
        Args:
            pos (str): The desired position.
            player (int): Player value.
        """
        self._board[int(pos[1:])][self._cols_labels.index(pos[0])] = player

    # Get Methods
    def get_tile(self, pos):
        """Get the player at this position.
        Args:
            pos (Any): Position of to examine
        Return:
            int: Player that occupies the cell.
        """
        if pos is list([int]):
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
        pos = ''.join([col_str, str(row)])

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

        square[0][0] = ''.join([self._cols_labels[col_neg], str(row_neg)])
        square[0][1] = ''.join([pos[0], str(row_neg)])
        square[0][2] = ''.join([self._cols_labels[col_pos], str(row_neg)])

        square[1][0] = ''.join([self._cols_labels[col_neg], str(pos[1:])])
        square[1][1] = pos
        square[1][2] = ''.join([self._cols_labels[col_pos], str(pos[1:])])

        square[2][0] = ''.join([self._cols_labels[col_neg], str(row_pos)])
        square[2][1] = ''.join([pos[0], str(row_pos)])
        square[2][2] = ''.join([self._cols_labels[col_pos], str(row_pos)])

        return square

    def print_footprint(self, foot):
        """Display the footprint.
        Args:
            foot (list[list[str]]): Footprint
        """

        print(foot[0][0] + "|" + foot[0][1] + "|" + foot[0][2])
        print("-----")
        print(foot[1][0] + "|" + foot[1][1] + "|" + foot[1][2])
        print("-----")
        print(foot[2][0] + "|" + foot[2][1] + "|" + foot[2][2])


class GessGame:
    """Class that implements the game of Gess."""
    def __init__(self):
        # DEBUG FLAG #
        self._DEBUG = False

        # Set the initial state
        self._board = Board()

        # Set Game state
        self._game_states = ['UNFINISHED', 'BLACK_WON', 'WHITE_WON']
        self._current_state = self._game_states[0]

        # Establish players
        self._player_list = dict()

        self._p1 = Player(1)
        self._p2 = Player(2)

        # Set the player default Rings
        self._player_list[self._p1.get_player()] = []
        self._player_list[self._p2.get_player()] = []

        self._player_list[self._p1.get_player()].append("l3")
        self._player_list[self._p2.get_player()].append("l18")

        # Set first turn
        self._turn = self._p1.get_player()

    # Get Methods
    def get_game_state(self):
        """Returns the current game state as a string."""
        return self._current_state

    def _next_turn(self):
        """Get the next player number.
        Returns:
            int: Player number.
        """
        if self._turn is self._p2.get_player():
            return self._p1.get_player()
        else:
            return self._p2.get_player()

    def _update_game_state(self):
        """Update the current game state."""

        # Get the next player
        nex_player = self._next_turn()

        # Check if the current player has made a new ring
        for row in range(1, 19):
            for col in range(1, 19):
                tile = self._board.get_position(row, col)
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
                        if check_tile is tile:
                            continue
                        if self._board.get_tile(check_tile) is self._turn:
                            ring += 1
                        if self._board.get_tile(check_tile) is nex_player:
                            opp_ring += 1

                if ring == 8:
                    self._player_list[self._turn].append(tile)
                if opp_ring == 8:
                    self._player_list[nex_player].append(tile)

        del check_foot, tile

        # If the next player is left without a ring, then the current player has won.
        rings = self._player_list[nex_player].copy()
        if len(rings) is 0:
            if nex_player is 0:
                self._current_state = self._game_states[1]
            else:
                self._current_state = self._game_states[2]

        del rings

    def resign_game(self):
        """A method for the current player to resign.
        Raises:
            PlayerNotValid: Player is not valid.
        """
        if self._turn == 1:
            if self._DEBUG:
                print("Black Resign")
            self._current_state = self._game_states[2]
        elif self._turn == 2:
            if self._DEBUG:
                print("White Resign")
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

        if self._DEBUG:
            print("Turn: " + str(self._turn) + ", Piece Selected: " + piece_pos + ", Destination: " + future_pos)

        col_destin = future_pos[0].lower()
        col_source = piece_pos[0].lower()
        nex_player = self._next_turn()

        # This block of checks evaluates the desired turn and establishes the validity of the turn
        # If the game has been won, the turn is invalid
        if self._current_state is (self._game_states[1] or self._game_states[2]):
            if self._DEBUG:
                print("Game Finished")
            return False
        # If the move is Out of Bounds, the turn is invalid
        if ((col_destin or col_source) is ['a', 't']) or ((piece_pos[1:] or future_pos[1:]) is ["0", "20"]):
            if self._DEBUG:
                print("Move OOB")
            return False
        # If the piece that the player has selected is not theirs, the turn is invalid
        if self._board.get_tile(piece_pos) is nex_player:
            if self._DEBUG:
                print("Invalid piece selection")
            return False
        # If the move leaves the current player without a ring, the move is invalid
        rings = self._player_list[self._turn].copy()
        for ring in rings:
            foot = self._board.footprint(ring)
            if piece_pos in foot:
                if self._DEBUG:
                    print("You would be without a ring")
                return False
        del rings, foot

        col_only = 0
        direction = 0

        # Set the direction flag
        if col_destin > col_source:
            direction = 1
        elif col_destin < col_source:
            direction = -1
        elif col_destin == col_source:
            col_only = 1

        # Check whether the destination is a valid move based on direction
        if direction is 0:
            if int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3)):
                if self._DEBUG:
                    print("Invalid direction")
                return False
        elif direction is -1:
            if (col_destin not in self._board.get_col_range(0, col_source)) & \
               (int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3))):
                if self._DEBUG:
                    print("Invalid direction")
                return False
        elif direction is 1:
            if (col_destin not in self._board.get_col_range(1, col_source)) & \
               (int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3))):
                if self._DEBUG:
                    print("Invalid direction")
                return False
        elif col_only is 1:
            if (col_destin not in self._board.get_col_range(1, col_source)) | \
               (col_destin not in self._board.get_col_range(0, col_source)):
                if self._DEBUG:
                    print("Invalid direction")
                return False
        elif col_only is 0:
            if int(future_pos[1:]) > ((int(piece_pos[1:]) + 3) | (int(piece_pos[1:]) - 3)):
                if self._DEBUG:
                    print("Invalid direction")
                return False
        else:
            raise AttributeError

        # Establish the current footprint
        source = self._board.footprint(piece_pos)

        # Create the destination footprint
        destin = self._board.footprint(future_pos)

        # Make the move
        # Determine there are any pieces making the move invalid
        for row in range(3):
            for col in range(3):

                source_tile = source[row][col]
                destin_tile = destin[row][col]

                # If the current current indexed tile is blocked, the turn is invalid
                if self._board.get_tile(source_tile) is nex_player:
                    if self._DEBUG:
                        print("Invalid footprint")
                    del source_tile, destin_tile
                    return False

                # If the current current indexed tile is blocked, the turn is invalid
                if (self._board.get_tile(destin_tile) is self._turn) & (self._board.get_tile(source_tile) is not 0):
                    if self._DEBUG:
                        print("Invalid Destination")
                    del source_tile, destin_tile
                    return False

                # Remove opponent tiles in the destination
                if self._board.get_tile(destin_tile) is nex_player:
                    self._board.set_tile(destin_tile, 0)
                # Set the tile to the current player
                else:
                    self._board.set_tile(destin_tile, self._turn)

        del source_tile, destin_tile

        # Update Game State
        self._update_game_state()

        # Pass the turn
        self._turn = nex_player

        return True
