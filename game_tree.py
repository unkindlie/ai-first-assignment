import copy
from collections import defaultdict
from game_state import NumberGame

class GameTree:
    def _init_(self):
        self.nodes = defaultdict(list)

    def add_node(self, state, level):
        state_repr = self.state_to_string(state, level)
        self.nodes[level].append(state_repr)

    def state_to_string(self, state, level):
        return f"{state.numbers} | H: {state.human_score} | C: {state.computer_score} | {state.current_player}"


def generate_game_tree(state, depth=3):
    tree = GameTree()

    def explore(state, depth, level):
        if depth == 0 or state.game_over:
            return

        tree.add_node(state, level)

        for index in range(len(state.numbers)):
            for move in state.get_legal_moves(index):
                new_state = copy.deepcopy(state)
                new_state.apply_move(index, move)
                tree.add_node(new_state, level + 1)
                explore(new_state, depth - 1, level + 1)

    explore(state, depth, 0)
    return tree


def print_game_tree(tree):
    print("Game tree nodes:")
    for level in sorted(tree.nodes.keys()):
        for node in tree.nodes[level]:
            print(f"Level {level}: {node}")

game = NumberGame(15)
game_tree = generate_game_tree(game, depth=3)
print_game_tree(game_tree)
