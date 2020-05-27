# Author: James Leflang
# Date: 06/04/2020
# Description: An implementation of the game Gess.


class PlayerNotValid(Exception):
    """Player object is not found."""
    pass


class LinkedList:
    """A linked list implementation of the List ADT. Meant to hold Player objects."""
    def __init__(self):
        self._head = None

    def _rec_contains(self, node, val):
        """A helper method for the contains method.
        Args:
            node (Any): Node object.
            val (int): Value for the node we are looking for.
        Returns:
            bool: Whether the desired value is in the list.
        """
        if self.is_empty():
            return False

        if node.get_player is val:
            return True

        if node.get_player is not val:
            return self._rec_contains(node.get_next, val)

    def contains(self, val):
        """Method to determine if this linked list has a particular value.
        Args:
            val (int): The desired value.
        Returns:
            bool: Whether the desired value is in the list.
        """

        current = self._head

        if current.get_player is val:
            return True

        if current.get_player is not val:
            return self._rec_contains(current.get_next, val)

    def _rec_add(self, val, cur_node):
        """Helper to add to the linked list.
        Args:
            val (int): Value to add.
            cur_node (Any): Current node.
        """
        current = cur_node
        if current.get_next() is not None:
            self._rec_add(val, current.get_next())
        else:
            new_player = Player(val)
            current.set_next(val)
            new_player.get_next()

    def add(self, val):
        """Adds a node containing val to the linked list.
        Args:
            val (int): Value to add.
        """
        if self._head is None:  # If the list is empty
            self._head = Player(val)
        else:
            current = self._head
            if current.get_next() is not None:
                self._rec_add(val, current.get_next())

    def is_empty(self):
        """Checks if the linked list is empty.
        Returns:
             bool: True if the linked list is empty, returns False otherwise
        """
        return self._head is None

    def _rec_to_regular_list(self, node, result):
        """Helper for to_regular_list.
        Args:
            node (Any): Current node.
            result (list[int]): The returned list.
        Returns:
            list[int]: The list of nodes.
        """
        if node is None:
            return result

        if node is not None:
            result += [node.get_player]
            self._rec_to_regular_list(node.get_next, result)

    def to_regular_list(self):
        """Returns a regular Python list containing the same values, in the same order, as the linked list.
        Returns:
            list[int]: The list of nodes.
        """
        result = []
        current = self._head
        if current is not None:
            result += [current.get_player]
            self._rec_to_regular_list(current.get_next, result)
        return result

    def next(self):
        """Returns the next player number as an int.
        Returns:
            int: Player value.
        """
        current = self._head

        if current.get_next() is not None:
            return current.get_next()
        else:
            return current.get_player()


class Player:
    """A Player object. Meant to be a node in a linked list.
    Args:
        player (int): The player number.
    """
    def __init__(self, player):
        self._player = player
        self._next = None

    # Get Methods
    def get_player(self):
        return self._player

    def get_next(self):
        return self._next

    # Set Method
    def set_next(self, nex):
        self._next = nex


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
    def set_player(self, pos, player):
        """Sets the desired position to the player.
        Args:
            pos (str): The desired position.
            player (int): Player value.
        """
        self._board[int(pos[0])][self._cols_labels.index(pos[0])] = player

    # Get Methods
    def get_player(self, pos):
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
        """
        col_str = self._cols_labels[col]
        pos = col_str.join(str(row))

        return pos

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

        self._player_list = list()

        self._player_list.append(Player(1))
        self._player_list.append(Player(2))

        # self._players = self._player_list.to_regular_list()

        self._game_states = ['UNFINISHED', 'BLACK_WON', 'WHITE_WON']
        self._current_state = self._game_states[0]

        # Set the player default Rings
        self._player_list[0] = self._board.footprint("l3")
        self._player_list[1] = self._board.footprint("l18")

        # Set first turn
        self._turn = self._next_turn()

    # Get Methods
    def get_game_state(self):
        """Returns the current game state as a string."""
        return self._current_state

    def _next_turn(self):
        """End a turn and hand a turn to the next player.
        Returns:
            int: Player number.
        """
        if (self._turn is None) | (self._turn is 1):
            return self._player_list[0]
        else:
            return self._player_list[1]

    def _update_game_state(self):
        """Update the current game state."""
        # TODO Develop the logic that allows for the determination of the game state and actually update it.
        pass

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

        # Local variables
        # FLAGS = [nw, n,         ne,
        #          w,  unlimited, e,
        #          sw, s,         se]
        flags = [0, 0, 0,
                 0, 0, 0,
                 0, 0, 0]

        # This block of checks evaluates the desired turn and establishes the validity of the turn
        # If the game has been won, the turn is invalid
        if self._current_state is (self._game_states[1] or self._game_states[2]):
            return False
        # If the move is Out of Bounds, the turn is invalid
        if (piece_pos[0] or future_pos[0] in 'at') or \
           ((piece_pos[1:] or future_pos[1:]) == 0 | 20):
            return False
        # If the piece that the player has selected is not theirs, the turn is invalid
        if self._board.get_player(piece_pos) is not self._turn:
            return False

        # Establish the current footprint
        source = self._board.footprint(piece_pos)

        # Determine valid move directions
        for row in source[:]:
            for col in row[:]:
                # If the current current indexed tile is owned by the opponent, the turn is invalid
                if self._board.get_player([col, row]) is not self._turn or 0:
                    return False

                # Set the appropriate flag for the available moves
                if self._board.get_player([row, col]) is self._turn:
                    if row and col == 0:
                        flags[0] = 1
                    elif row and col == 1:
                        flags[4] = 1
                    elif row and col == 2:
                        flags[8] = 1
                    elif row == 0 and col == 1:
                        flags[1] = 1
                    elif row == 0 and col == 2:
                        flags[2] = 1
                    elif row == 1 and col == 0:
                        flags[3] = 1
                    elif row == 1 and col == 2:
                        flags[5] = 1
                    elif row == 2 and col == 0:
                        flags[6] = 1
                    elif row == 2 and col == 1:
                        flags[7] = 1

        # Create the destination footprint
        destin = self._board.footprint(future_pos)

        # TODO Check whether the destination is a valid move based on the current footprint.

        # Place the pieces in the destination
        for row in destin[:]:
            for tile in row[:]:
                # Get the owner
                self._board.set_player(tile, self._turn)

        # TODO Need to adequately deal with captures and updating the game state.

        # Update Game State
        self._update_game_state()

        # Pass the turn
        self._turn = self._next_turn()

        return True
