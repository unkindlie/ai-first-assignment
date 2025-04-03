import math
import copy

class GameAI:
    def __init__(self, game, algorithm='minimax', depth=3):
        # Initializing the GameAI class
        self.game = game  # The current game state
        self.algorithm = algorithm  # Algorithm to use ('minimax' or 'alpha-beta')
        self.depth = depth  # Depth of the search tree

    def minimax(self, state, depth, maximizing_player):
        # Minimax algorithm 
        if depth == 0 or state.game_over:  # Base case
            return state.computer_score - state.human_score  # Return score difference

        if maximizing_player:
            max_eval = -math.inf  # Initialize max evaluation to negative infinity
            for index in range(len(state.numbers)):  # Iterate over all indices
                for move in state.get_legal_moves(index):  # Iterate over legal moves
                    new_state = copy.deepcopy(state)  # Create a deep copy of the state
                    new_state.apply_move(index, move)  # Apply the move to the new state
                    eval = self.minimax(new_state, depth-1, False)  # Recursive call for minimizing player
                    max_eval = max(max_eval, eval)  # Update max evaluation
            return max_eval
        else:
            min_eval = math.inf  # Initialize min evaluation to positive infinity
            for index in range(len(state.numbers)):  # Iterate over all indices
                for move in state.get_legal_moves(index):  # Iterate over legal moves
                    new_state = copy.deepcopy(state)  # Create a deep copy of the state
                    new_state.apply_move(index, move)  # Apply the move to the new state
                    eval = self.minimax(new_state, depth-1, True)  # Recursive call for maximizing player
                    min_eval = min(min_eval, eval)  # Update min evaluation
            return min_eval
        
    def alpha_beta(self, state, depth, alpha, beta, maximizing_player):
        # Alpha-beta pruning algorithm 
        if depth == 0 or state.game_over:
            return state.computer_score - state.human_score  # Return score difference

        if maximizing_player:
            max_eval = -math.inf  # Initialize max evaluation to negative infinity
            for index in range(len(state.numbers)):  # Iterate over all indices
                for move in state.get_legal_moves(index):  # Iterate over legal moves
                    new_state = copy.deepcopy(state)  # Create a deep copy of the state
                    new_state.apply_move(index, move)  # Apply the move to the new state
                    eval = self.alpha_beta(new_state, depth-1, alpha, beta, False)  # Recursive call for minimizing player
                    max_eval = max(max_eval, eval)  # Update max evaluation
                    alpha = max(alpha, eval)  # Update alpha value
                    if beta <= alpha:  # Prune the branch if beta <= alpha
                        break
            return max_eval
        else:
            min_eval = math.inf  # Initialize min evaluation to positive infinity
            for index in range(len(state.numbers)):  # Iterate over all indices
                for move in state.get_legal_moves(index):  # Iterate over legal moves
                    new_state = copy.deepcopy(state)  # Create a deep copy of the state
                    new_state.apply_move(index, move)  # Apply the move to the new state
                    eval = self.alpha_beta(new_state, depth-1, alpha, beta, True)  # Recursive call for maximizing player
                    min_eval = min(min_eval, eval)  # Update min evaluation
                    beta = min(beta, eval)  # Update beta value
                    if beta <= alpha:  # Prune the branch if beta <= alpha
                        break
            return min_eval

    def get_best_move(self):
        # Determine the best move for the current player
        best_score = -math.inf  # Initialize best score to negative infinity
        best_move = None  # Initialize best move to None
        best_index = 0  # Initialize best index to 0

        for index in range(len(self.game.numbers)):  # Iterate over all indices
            for move in self.game.get_legal_moves(index):  # Iterate over legal moves
                new_game = copy.deepcopy(self.game)  # Create a deep copy of the game state
                new_game.apply_move(index, move)  # Apply the move to the new game state
                
                if self.algorithm == 'minimax':
                    score = self.minimax(new_game, self.depth-1, False)  # Call minimax
                else:  # If the algorithm is alpha-beta pruning
                    score = self.alpha_beta(new_game, self.depth-1, -math.inf, math.inf, False)  # Call alpha-beta

                if score > best_score: 
                    best_score = score
                    best_move = move
                    best_index = index

        return best_index, best_move 

