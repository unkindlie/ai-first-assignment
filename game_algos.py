import math
import copy

class GameAI:
    def __init__(self, game, algorithm='minimax', depth=3):
        self.game = game
        self.algorithm = algorithm
        self.depth = depth

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.game_over:
            return state.computer_score - state.human_score

        if maximizing_player:
            max_eval = -math.inf
            for index in range(len(state.numbers)):
                for move in state.get_legal_moves(index):
                    new_state = copy.deepcopy(state)
                    new_state.apply_move(index, move)
                    eval = self.minimax(new_state, depth-1, False)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for index in range(len(state.numbers)):
                for move in state.get_legal_moves(index):
                    new_state = copy.deepcopy(state)
                    new_state.apply_move(index, move)
                    eval = self.minimax(new_state, depth-1, True)
                    min_eval = min(min_eval, eval)
            return min_eval
        
    def alpha_beta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.game_over:
            return state.computer_score - state.human_score

        if maximizing_player:
            max_eval = -math.inf
            for index in range(len(state.numbers)):
                for move in state.get_legal_moves(index):
                    new_state = copy.deepcopy(state)
                    new_state.apply_move(index, move)
                    eval = self.alpha_beta(new_state, depth-1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = math.inf
            for index in range(len(state.numbers)):
                for move in state.get_legal_moves(index):
                    new_state = copy.deepcopy(state)
                    new_state.apply_move(index, move)
                    eval = self.alpha_beta(new_state, depth-1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        best_index = 0

        for index in range(len(self.game.numbers)):
            for move in self.game.get_legal_moves(index):
                new_game = copy.deepcopy(self.game)
                new_game.apply_move(index, move)
                
                if self.algorithm == 'minimax':
                    score = self.minimax(new_game, self.depth-1, False)
                else:
                    score = self.alpha_beta(new_game, self.depth-1, -math.inf, math.inf, False)

                if score > best_score:
                    best_score = score
                    best_move = move
                    best_index = index

        return best_index, best_move

