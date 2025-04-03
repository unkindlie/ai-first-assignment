import copy
from collections import defaultdict
from game_state import NumberGame

class GameTree:
    # Initialization of the dictionary
    def __init__(self):
        self.nodes = defaultdict(list)

    def add_node(self, state, level):
        state_repr = self.state_to_string(state)
        self.nodes[level].append(state_repr)

    # Interpolate the node to the string
    @staticmethod
    def state_to_string(state):
        return f"{state.numbers} | H: {state.human_score} | C: {state.computer_score} | {state.current_player}"

def generate_game_tree(state, depth=3):
    tree = GameTree()

    # Embedded recursive function that checks the possible moves
    def explore(state, depth, level):
        if depth == 0 or state.game_over:
            return

        tree.add_node(state, level)

        # Exploring each possible move
        for index in range(len(state.numbers)):
            for move in state.get_legal_moves(index):
                # Creating new state
                new_state = copy.deepcopy(state)
                new_state.apply_move(index, move)
                # Adding it with the applied moves
                tree.add_node(new_state, level + 1)
                # Another recursive exploration
                explore(new_state, depth - 1, level + 1)

    # exploring from the root state
    explore(state, depth, 0)
    return tree

def print_game_tree(tree):
    print("Game tree nodes:")

    # Printing the nodes sorted by level
    for level in sorted(tree.nodes.keys()):
        for node in tree.nodes[level]:
            print(f"Level {level}: {node}")

game = NumberGame(15)
game_tree = generate_game_tree(game, depth=4)
print_game_tree(game_tree)
