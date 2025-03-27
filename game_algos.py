class GameAI:
    def __init__(self, game, algorithm='minimax', depth=3):
        self.game = game
        self.algorithm = algorithm
        self.depth = depth

    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.game_over:
            return state.computer_score - state.human_score

        if maximizing_player
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
