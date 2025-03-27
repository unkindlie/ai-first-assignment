import tkinter as tk
from tkinter import messagebox, simpledialog
from game_state import NumberGame
from game_algos import GameAI

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Number Game")
        
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
        
        self.game = None
        self.ai = None
        self.player_start = 'human'
        self.algorithm = 'minimax'

    def initialize_game(self):
        length = simpledialog.askinteger("Game Length", "Enter string length (15-20):", 
                                       parent=self.master, minvalue=15, maxvalue=20)
        if not length: return
        
        self.player_start = messagebox.askquestion("First Player", 
                                                  "Should human start first?") == 'yes'
        self.algorithm = 'alphabeta' if messagebox.askquestion("Algorithm", 
                                                             "Use Alpha-Beta pruning? Click no for Minimax") == 'yes' else 'minimax'
        
        self.game = NumberGame(length)
        self.ai = GameAI(self.game, self.algorithm)
        self.game.current_player = 'human' if self.player_start else 'computer'
        
        self.update_display()
        
        if not self.player_start:
            self.computer_move()
