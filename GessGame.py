# Author: James Leflang
# Date: 06/04/2020
# Description: An implementation of the game Gess.


class PlayerNotValid(Exception):
    """Player object is not found."""
    pass


class LinkedList:
    """
    A linked list implementation of the List ADT
    """
    def __init__(self):
        self._head = None

    def _rec_contains(self, node, val):
        """
        A helper method for the contains method
        """
        if self.is_empty():
            return False

        if node.get_player is val:
            return True

        if node.get_player is not val:
            return self._rec_contains(node.get_next, val)

    def contains(self, val):
        """
        Method to determine if this linked list has a particular value
        """

        current = self._head

        if current.get_player is val:
            return True

        if current.get_player is not val:
            return self._rec_contains(current.get_next, val)

    def _rec_add(self, val, cur_node):
        """"""
        current = cur_node
        if current.get_next() is not None:
            self._rec_add(val, current.get_next())
        else:
            new_player = Player(val)
            current.set_next(val)
            new_player.get_next()

    def add(self, val):
        """
        Adds a node containing val to the linked list
        """
        if self._head is None:  # If the list is empty
            self._head = Player(val)
        else:
            current = self._head
            if current.get_next() is not None:
                self._rec_add(val, current.get_next())

    def is_empty(self):
        """
        Returns True if the linked list is empty,
        returns False otherwise
        """
        return self._head is None

    def _rec_to_regular_list(self, node, result):
        """
        Returns a regular Python list containing the same values, in the same order, as the linked list
        """
        if node is None:
            return result

        if node is not None:
            result += [node.get_player]
            self._rec_to_regular_list(node.get_next, result)

    def to_regular_list(self):
        """
        Returns a regular Python list containing the same values, in the same order, as the linked list
        """
        result = []
        current = self._head
        if current is not None:
            result += [current.get_player]
            self._rec_to_regular_list(current.get_next, result)
        return result

    def next(self):
        """
        Returns the next player number as an int
        """
        current = self._head

        if current.get_next() is not None:
            return current.get_next()
        else:
            return current.get_player()


class Player:
    """A Player object.
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
    """A Board object."""
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
        self._board[self._cols_labels.index(pos[0])][int(pos[1:])] = player

    # Get Method
    def get_player(self, pos):
        row = None
        col = None

        if pos is int:
            row = pos[0]
            col = pos[1]
        else:
            row = self._cols_labels.index(pos[0])
            col = int(pos[1:])

        return self._board[row][col]

    # def get_position(self, pos):
    #     row = self._cols_labels.index(pos[0])
    #     col = int(pos[1:])
    #
    #     return [row, col]


class GessGame:
    """Class that implements the game of Gess."""
    def __init__(self):
        # Set the initial state
        self._board = Board()

        self._player_list = LinkedList()

        self._player_list.add(1)
        self._player_list.add(2)

        self._players = self._player_list.to_regular_list()

        self._game_states = ['UNFINISHED', 'BLACK_WON', 'WHITE_WON']
        self._current_state = self._game_states[0]

        # Set first turn
        self._turn = self._next_turn()

    # Get Methods
    def get_game_state(self):
        return self._current_state

    def _next_turn(self):
        """End a turn and hand a turn to the next player.
        Returns:
            int: Player number.
        """
        if self._turn is None:
            return self._players[0]
        else:
            self._player_list.next()

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

        # If the game has been won, the turn is invalid
        if self._current_state is (self._game_states[1] or self._game_states[2]):
            return False
        # If the move is oob
        if (piece_pos[0] or future_pos[0] in 'at') or \
           ((piece_pos[1] or future_pos[1]) == 0 | 20):
            return False

        square = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]

        for ind, row in square[:]:
            for col in row[:]:
                # If the current current indexed tile is owned by the opponent, the turn is invalid
                if self._board.get_player([ind, col]) is not self._turn or 0:
                    return False
                # Get the owner
                square[ind][col] = self._board.get_player([ind, col])

        # Pass the turn
        self._turn = self._next_turn()

        return True
