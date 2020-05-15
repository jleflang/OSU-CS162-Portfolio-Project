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

    def rec_contains(self, node, val):
        """
        A helper method for the contains method
        """
        if self.is_empty():
            return False

        if node.get_player is val:
            return True

        if node.get_player is not val:
            return self.rec_contains(node.get_next, val)

    def contains(self, val):
        """
        Method to determine if this linked list has a particular value
        """

        current = self._head

        if current.get_player is val:
            return True

        if current.get_player is not val:
            return self.rec_contains(current.get_next, val)

    def add(self, val):
        """
        Adds a node containing val to the linked list
        """
        if self._head is None:  # If the list is empty
            self._head = Player(val)
        else:
            current = self._head
            if current.get_next is not None:
                self.add(current.set_next)

    def is_empty(self):
        """
        Returns True if the linked list is empty,
        returns False otherwise
        """
        return self._head is None

    def rec_to_regular_list(self, node, result):
        """
        Returns a regular Python list containing the same values, in the same order, as the linked list
        """
        if node is None:
            return result

        if node is not None:
            result += [node.get_player]
            self.rec_to_regular_list(node.get_next, result)

    def to_regular_list(self):
        """
        Returns a regular Python list containing the same values, in the same order, as the linked list
        """
        result = []
        current = self._head
        if current is not None:
            result += [current.get_player]
            self.rec_to_regular_list(current.get_next, result)
        return result


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
        self._board[pos[0]][pos[1]] = player

    # Get Method
    def get_player(self, pos):
        col = self._cols_labels.index(pos[0])
        row = pos[1]

        return self._board[col][row]


class GessGame:

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
        Raises:
            PlayerNotValid: Player is not valid.
        """
        if self._turn is None:
            return self._players[0]
        elif self._turn == 2:
            return self._players[0]
        elif self._turn == 1:
            return self._players[1]
        else:
            raise PlayerNotValid

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

        # If the current player does not possess the piece, the turn is invalid
        if self._turn is not self._board.get_player(piece_pos):
            return False
        # If the game has been won, the turn is invalid
        if self._current_state is (self._game_states[1] or self._game_states[2]):
            return False

        # Pass the turn
        self._turn = self._next_turn()

        return True
