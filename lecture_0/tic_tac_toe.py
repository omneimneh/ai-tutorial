from enum import Enum
from typing import List, Tuple
from copy import deepcopy


class TicTacPlayer(Enum):
    X = 0
    O = 1


class TicTacGame:

    def __init__(self, board: List[List[int]] = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ], moves: int = 0):
        self.board = board
        self.moves = moves

    def display(self):
        for row in self.board:
            for col in row:
                print('.' if col is None else str(col)[-1], end='')
            print()

    def is_empty(self) -> bool:
        for row in self.board:
            for col in row:
                if col is not None:
                    return False
        return True

    def has_ended(self) -> bool:
        filled = True
        for row in self.board:
            for col in row:
                if col is None:
                    filled = False

        if filled:
            return True

        if self.winner() is None:
            return False
        return True

    def winner(self) -> TicTacPlayer:
        # check row
        for row in self.board:
            if all([col is TicTacPlayer.X for col in row]):
                return TicTacPlayer.X
            if all([col is TicTacPlayer.O for col in row]):
                return TicTacPlayer.O

        # check col
        for i in range(len(self.board)):
            if all([row[i] is TicTacPlayer.X for row in self.board]):
                return TicTacPlayer.X
            if all([row[i] is TicTacPlayer.O for row in self.board]):
                return TicTacPlayer.O

        # check diagonal
        if all([self.board[i][i] is TicTacPlayer.X for i in range(len(self.board))]):
            return TicTacPlayer.X
        if all([self.board[i][i] is TicTacPlayer.O for i in range(len(self.board))]):
            return TicTacPlayer.O

        if all([self.board[i][2 - i] is TicTacPlayer.X for i in range(len(self.board))]):
            return TicTacPlayer.X
        if all([self.board[i][2 - i] is TicTacPlayer.O for i in range(len(self.board))]):
            return TicTacPlayer.O

        return None

    def play(self, x: int, y: int) -> bool:
        if x < 0 or x > 2 or y < 0 or y > 2 or self.board[x][y] is not None:
            return False

        self.board[x][y] = self.turn()
        self.moves += 1

        return True

    def turn(self) -> TicTacPlayer:
        return TicTacPlayer.X if self.moves % 2 is 0 else TicTacPlayer.O

    def copy(self):
        return TicTacGame(deepcopy(self.board), self.moves)


class TicTacAgent:
    def __init__(self, game: TicTacGame, turn: TicTacPlayer):
        self.game = game
        self.turn = turn

    def play(self):
        if(self.game.is_empty()):
            return (0, 0, 0)
        if self.turn is TicTacPlayer.X:
            return self.max_min(self.game)
        else:
            return self.min_max(self.game)

    def min_max(self, game: TicTacGame):
        if game.has_ended():
            winner = game.winner()
            if winner is None:
                return (0, -1, -1)
            return (1, -1, -1) if winner is TicTacPlayer.X else (-1, -1, -1)

        res, resI, resJ = 100, -1, -1
        for i in range(len(game.board)):
            for j in range(len(game.board)):
                copied_game = TicTacGame.copy(game)
                if copied_game.play(i, j):
                    computed = self.max_min(copied_game)[0]
                    if computed < res:
                        res, resI, resJ = computed, i, j

        return (res, resI, resJ)

    def max_min(self, game: TicTacGame):
        if game.has_ended():
            winner = game.winner()
            if winner is None:
                return (0, -1, -1)
            return (1, -1, -1) if winner is TicTacPlayer.X else (-1, -1, -1)

        res, resI, resJ = -100, -1, -1
        for i in range(len(game.board)):
            for j in range(len(game.board)):
                copied_game = TicTacGame.copy(game)
                if copied_game.play(i, j):
                    computed = self.min_max(copied_game)[0]
                    if computed > res:
                        res, resI, resJ = computed, i, j

        return (res, resI, resJ)


if __name__ == "__main__":
    user_turn = TicTacPlayer.O

    game = TicTacGame()
    agent = TicTacAgent(
        game, TicTacPlayer.X if user_turn is TicTacPlayer.O else TicTacPlayer.O)

    while not game.has_ended():
        game.display()
        print(f'{game.turn()} turns:')

        if game.turn() is user_turn:
            success = False
            while not success:
                x, y = int(input('select row (between 0-2): ')
                           ), int(input('select col (between 0-2): '))
                success = game.play(x, y)
        else:
            print('agent is thinking...')
            res, x, y = agent.play()
            game.play(x, y)

    print(f'{game.winner()} has won the game')
    game.display()
