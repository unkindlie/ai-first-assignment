import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from game_state import NumberGame
from game_algos import GameAI

class GameGUI:
    def __init__(self, master):
        # Initialization of the window from the parameter
        self.master = master
        self.master.title("Number Game")

        # Adding needed frames (containers), buttons and labels
        self.options_frame = tk.Frame(master)
        self.options_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.options_frame, text="New Game", command=self.initialize_game)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.numbers_frame = tk.Frame(master)
        self.numbers_frame.pack(pady=20)
        
        self.score_frame = tk.Frame(master)
        self.score_frame.pack(pady=10)
        
        self.human_score_label = tk.Label(self.score_frame, text="Human: 0")
        self.human_score_label.pack(side=tk.LEFT, padx=10)
        
        self.computer_score_label = tk.Label(self.score_frame, text="Computer: 0")
        self.computer_score_label.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack(pady=10)

        # Definition of properties for the game (with default values)
        self.game = None
        self.ai = None
        self.player_start = 'human'
        self.algorithm = 'minimax'

    def initialize_game(self):
        # Getting the length of the string from the dialog
        length = simpledialog.askinteger("Game Length", "Enter string length (15-20):", 
                                       parent=self.master, minvalue=15, maxvalue=20)
        if not length: return

        # Deciding the starter player of the game
        self.player_start = messagebox.askquestion("First Player", 
                                                  "Should human start first?") == 'yes'
        # Choosing the algorithm
        self.algorithm = 'alphabeta' if messagebox.askquestion("Algorithm", 
                                                             "Use Alpha-Beta pruning? Click no for Minimax") == 'yes' else 'minimax'
        # Initialization of the properties
        self.game = NumberGame(length)
        self.ai = GameAI(self.game, self.algorithm)
        self.game.current_player = 'human' if self.player_start else 'computer'
        
        self.update_display()
        
        if not self.player_start:
            self.computer_move()

    # Updating the UI
    def update_display(self):
        # Destroying the old number buttons
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()

        # Replacing with new number buttons
        for i, num in enumerate(self.game.numbers):
            btn = tk.Button(self.numbers_frame, text=str(num), width=3,
                            command=lambda idx=i: self.handle_click(idx))
            btn.pack(side=tk.LEFT, padx=2)

        # Updating the text of scores
        self.human_score_label.config(text=f"Human: {self.game.human_score}")
        self.computer_score_label.config(text=f"Computer: {self.game.computer_score}")

        # Updating the status of the game
        status = f"Current Player: {self.game.current_player.capitalize()}"
        if self.game.game_over:
            status = self.get_game_result()
        self.status_label.config(text=status)

    # Handling the click
    def handle_click(self, index):
        if self.game.game_over or self.game.current_player != 'human':
            return

        # Getting the possible moves for the node
        moves = self.game.get_legal_moves(index)
        if not moves:
            return

        # Adding possible choices
        menu = tk.Menu(self.master, tearoff=0)
        for move in moves:
            if move[0] == 'take':
                menu.add_command(label=f"Take {move[1]}",
                                 command=lambda m=move: self.apply_human_move(index, m))
            elif move[0] == 'split2':
                menu.add_command(label="Split 2 into 1+1",
                                 command=lambda m=move: self.apply_human_move(index, m))
            elif move[0] == 'split4':
                menu.add_command(label="Split 4 into 2+2 (+1 point)",
                                 command=lambda m=move: self.apply_human_move(index, m))

        menu.tk_popup(self.master.winfo_pointerx(), self.master.winfo_pointery())

    def apply_human_move(self, index, move):
        self.game.apply_move(index, move)
        self.update_display()

        if not self.game.game_over:
            self.computer_move()

    def computer_move(self):
        if self.game.game_over or self.game.current_player != 'computer':
            return

        self.status_label.config(text="Computer is thinking...")
        self.master.update()

        # Starting the timer
        start_time = time.time()
        index, move = self.ai.get_best_move()
        self.game.apply_move(index, move)

        # Checking the computer's time
        self.status_label.config(text=f"Computer moved in {time.time() - start_time:.1f}s")
        self.update_display()

    def get_game_result(self):
        human = self.game.human_score
        computer = self.game.computer_score

        if human > computer:
            return "Human wins!"
        elif computer > human:
            return "Computer wins!"
        else:
            return "It's a tie!"
