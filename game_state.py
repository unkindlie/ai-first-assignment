import random

class NumberGame:
    def __init__(self, length=15):
        self.numbers = [random.choice([1, 2, 3, 4]) for _ in range(length)]
        self.human_score = 0
        self.computer_score = 0
        self.current_player = 'human'
        self.game_over = False  # Game starts not over

    def get_legal_moves(self, index):
        moves = []
        num = self.numbers[index]
        moves.append(('take', num))
        if num == 2:
            moves.append(('split2',))
        elif num == 4:
            moves.append(('split4',))
        return moves

    def apply_move(self, index, move):
     # Apply a move to the game state at a specific index and added if else loops according to game play
        num = self.numbers[index]
        if move[0] == 'take':
            if self.current_player == 'human':
                self.human_score += num
            else:
                self.computer_score += num
            self.numbers.pop(index)
        elif move[0] == 'split2':
            self.numbers[index:index+1] = [1, 1]
        elif move[0] == 'split4':
            self.numbers[index:index+1] = [2, 2]
            if self.current_player == 'human':
                self.human_score += 1
            else:
                self.computer_score += 1

        self.current_player = 'computer' if self.current_player == 'human' else 'human'
        self.game_over = len(self.numbers) == 0
