import math
import random


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\' Twoja kolej. Input rusz się o (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Nieprawidłowy kwadrat. Spróbuj ponownie. ')
        return val


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['pozycja']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'pozycja': None, 'wynik': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'pozycja': None, 'wynik': 0}

        if player == max_player:
            best = {'pozycja': None, 'wynik': -math.inf}  
        else:
            best = {'pozycja': None, 'wynik': math.inf}  
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['pozycja'] = possible_move

            if player == max_player:
                if sim_score['wynik'] > best['wynik']:
                    best = sim_score
            else:
                if sim_score['wynik'] < best['wynik']:
                    best = sim_score
        return best