"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("+inf")

    return increasing_ferocity(game, player)


# def minimise_other_player(game, player):
#
#     other_player = game.__player_2__
#     if player == game.__player_2__:
#         other_player = game.__player_1__
#
#     return -len(game.get_legal_moves(other_player))
#
#
# def proximate_to_opponent(game, player):
#
#     other_player = game.__player_2__
#     if player == game.__player_2__:
#         other_player = game.__player_1__
#
#     pr, pc = game.get_player_location(player)
#     opr, opc = game.get_player_location(other_player)
#
#     distance_from_conceptual_border = ((pr - opr) * (pr - opr) + (pc - opc) * (pc - opc))
#     if distance_from_conceptual_border == 0:
#         return float("+inf")
#     return float(1 / distance_from_conceptual_border)
#
#
# def ratio_self_to_other(game, player):
#
#     other_player = game.__player_2__
#     if player == game.__player_2__:
#         other_player = game.__player_1__
#
#     number_player_moves = len(game.get_legal_moves(player))
#     number_other_player_moves = len(game.get_legal_moves(other_player))
#     if number_other_player_moves < 1:
#         return float("+inf")
#     else:
#         return float(number_player_moves) / float(number_other_player_moves)


def increasing_ferocity(game, player):

    ferocity = 1
    spaces = game.width * game.height
    blank_spaces = len(game.get_blank_spaces())

    complete_ratio = float(blank_spaces / spaces)

    if complete_ratio > 0.5:
        ferocity = 1.5

    if complete_ratio > 0.75:
        ferocity = 2

    if complete_ratio > 0.825:
        ferocity = 3

    other_player = game.__player_2__
    if player == game.__player_2__:
        other_player = game.__player_1__

    number_moves = len(game.get_legal_moves(player)) - ferocity * len(game.get_legal_moves(other_player))
    return float(number_moves)

#
# def other_player_squared_difference_score(game, player):
#
#     other_player = game.__player_2__
#     if player == game.__player_2__:
#         other_player = game.__player_1__
#
#     number_player_moves = len(game.get_legal_moves(player))
#     number_other_player_moves = len(game.get_legal_moves(other_player))
#     number_moves = number_player_moves - (number_other_player_moves * number_other_player_moves)
#     return float(number_moves)
#
#
# def posn_str(posn):
#     r, c = posn
#     return str(r) + "," + str(c)
#
#
# def map_partition(game, posn, opp_posn):
#
#     partition_space_strings = [posn_str(posn)]
#     partition_spaces = [posn]
#     directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
#
#     new_spaces = True
#     index = 0
#     while new_spaces:
#         new_spaces = False
#         count = len(partition_spaces)
#         for n in range(index, count):
#             for m in directions:
#                 r, c = partition_spaces[n]
#                 dr, dc = m
#                 new_pos = r + dr, c + dc
#                 new_pos_str = posn_str(new_pos)
#
#                 if (game.move_is_legal(new_pos) or new_pos == posn or new_pos == opp_posn) and new_pos_str not in partition_space_strings:
#                     partition_spaces.append(new_pos)
#                     partition_space_strings.append(new_pos_str)
#                     new_spaces = True
#         index = count
#
#     return partition_spaces, partition_space_strings
#
#
# def parity_advantage(game, player):
#
#     number_moves = len(game.get_legal_moves(player))
#
#     game_size = game.width * game.height
#     odd_game_size = is_odd(game_size)
#
#     number_blank_spaces = len(game.get_blank_spaces())
#     odd_blank_spaces = is_odd(number_blank_spaces)
#
#     opposite_parity = odd_game_size != odd_blank_spaces
#
#     if opposite_parity:
#         return 1000. * number_moves
#     else:
#         return number_moves
#
#
# def test_partition(game, player):
#
#     other_player = game.__player_2__
#     if player == game.__player_2__:
#         return 0.
#         other_player = game.__player_1__
#
#     score = other_player_squared_difference_score(game, player)
#
#     player_pos = game.get_player_location(player)
#     opponent_position = game.get_player_location(other_player)
#
#     partition_spaces, partition_space_strings = map_partition(game, player_pos, opponent_position)
#     own_freedom = len(partition_spaces)
#
#     if posn_str(opponent_position) in partition_space_strings:
#         if is_odd(own_freedom):
#             result = 2 * score
#         else:
#             result = score
#
#     else:
#         partition_spaces, partition_space_strings = map_partition(game, opponent_position, player_pos)
#         opponent_freedom = len(partition_spaces)
#
#         if own_freedom > opponent_freedom:
#             result = float("+inf")
#         else:
#             result = float("-inf")
#
#     return result
#
#
# def is_odd(number):
#
#     return number != 2 * int(number / 2)
#


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        best_score = float("-inf")
        best_move = (-1, -1)

        if len(legal_moves) < 1:
            return best_move

        self.TIMER_THRESHOLD = 50

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            if not self.iterative and self.method == "minimax":
                for move in legal_moves:
                    next_game = game.forecast_move(move)
                    score, _ = self.minimax(next_game, self.search_depth, False)
                    if score > best_score:
                        best_score = score
                        best_move = move

            elif not self.iterative and self.method == "alphabeta":
                for move in legal_moves:
                    next_game = game.forecast_move(move)
                    score, _ = self.alphabeta(next_game, self.search_depth, float("-inf"), float("+inf"), False)
                    if score > best_score:
                        best_score = score
                        best_move = move

            elif self.iterative and self.method == "minimax":
                depth = self.search_depth
                while True:
                    for move in legal_moves:
                        score, _ = self.minimax(game.forecast_move(move), depth, False)
                        if score > best_score:
                            best_move = move
                            best_score = score
                    depth += 1

            elif self.iterative and self.method == "alphabeta":
                depth = self.search_depth
                while True:
                    for move in legal_moves:
                        score, _ = self.alphabeta(game.forecast_move(move), depth, float("-inf"), float("+inf"), False)
                        if score > best_score:
                            best_move = move
                            best_score = score
                    depth += 1

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!

        if depth == 0:
            return self.score(game, self), game.__last_player_move__

        best_move = (-1, -1)
        best_value = float("-inf")
        if not maximizing_player:
            best_value = float("+inf")

        moves = game.get_legal_moves()

        for move in moves:
            try_game = game.forecast_move(move)
            value, _ = self.minimax(try_game, depth - 1, not maximizing_player)
            if maximizing_player and value > best_value:
                best_value = value
                best_move = move
            elif not maximizing_player and value < best_value:
                best_value = value
                best_move = move

        return best_value, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!

        if depth == 0:
            value = self.score(game, game.active_player)
            return value, game.__last_player_move__

        moves = game.get_legal_moves()

        if maximizing_player:

            value = float("-inf")
            move = (-1, -1)
            for m in moves:
                try_game = game.forecast_move(m)
                move_value, _ = self.alphabeta(try_game, depth - 1, alpha, beta, False)
                if move_value > value:
                    move = m
                    value = move_value
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value, move

        else:

            value = float("+inf")
            move = (-1, -1)
            for m in moves:
                try_game = game.forecast_move(m)
                move_value, _ = self.alphabeta(try_game, depth - 1, alpha, beta, True)
                if move_value < value:
                    move = m
                    value = move_value
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, move
