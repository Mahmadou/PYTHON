import tkinter as tk
from tkinter import messagebox
import random
from enum import Enum
from typing import List, Tuple, Optional
import time

class CellState(Enum):
    """États possibles d'une cellule du plateau"""
    EMPTY = "white"
    SHIP = "gray"
    HIT = "red"
    MISS = "blue"
    SUNK = "black"

class Ship:
    """Représentation d'un navire"""
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.positions: List[Tuple[int, int]] = []
        self.hits: List[bool] = []
        
    def place(self, positions: List[Tuple[int, int]]):
        self.positions = positions
        self.hits = [False] * self.size
        
    def hit(self, position: Tuple[int, int]) -> bool:
        if position in self.positions:
            self.hits[self.positions.index(position)] = True
            return True
        return False
        
    @property
    def is_sunk(self) -> bool:
        return all(self.hits)

class Board:
    """Plateau de jeu"""
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        
    def can_place_ship(self, ship: Ship, start: Tuple[int, int], horizontal: bool) -> bool:
        x, y = start
        if horizontal:
            if y + ship.size > self.size:
                return False
            return all(self.grid[x][y+i] == CellState.EMPTY for i in range(ship.size))
        else:
            if x + ship.size > self.size:
                return False
            return all(self.grid[x+i][y] == CellState.EMPTY for i in range(ship.size))
    
    def place_ship(self, ship: Ship, start: Tuple[int, int], horizontal: bool) -> bool:
        if not self.can_place_ship(ship, start, horizontal):
            return False
            
        x, y = start
        positions = []
        if horizontal:
            positions = [(x, y+i) for i in range(ship.size)]
        else:
            positions = [(x+i, y) for i in range(ship.size)]
            
        ship.place(positions)
        for pos in positions:
            self.grid[pos[0]][pos[1]] = CellState.SHIP
            
        self.ships.append(ship)
        return True
        
    def receive_attack(self, position: Tuple[int, int]) -> Tuple[bool, Optional[Ship]]:
        x, y = position
        if self.grid[x][y] == CellState.SHIP:
            self.grid[x][y] = CellState.HIT
            for ship in self.ships:
                if ship.hit(position):
                    if ship.is_sunk:
                        for pos in ship.positions:
                            self.grid[pos[0]][pos[1]] = CellState.SUNK
                        return True, ship
                    return True, None
        else:
            self.grid[x][y] = CellState.MISS
        return False, None

    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk for ship in self.ships)

class BattleshipGame:
    """Gestion du jeu de bataille navale"""
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Bataille Navale")
        
        self.player_board = Board()
        self.computer_board = Board()
        self.game_started = False
        self.player_turn = True
        
        self.ship_types = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2)
        ]
        
        self.ships_to_place = self.ship_types.copy()
        self.current_orientation = True
        self.initialize_ui()

    def initialize_ui(self):
        """Initialisation de l'interface utilisateur"""
        # Frame de contrôle
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=10)
        
        # Boutons de contrôle
        self.new_game_btn = tk.Button(control_frame, text="Nouvelle Partie", command=self.start_new_game)
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        self.orientation_btn = tk.Button(control_frame, text="Changer Orientation", command=self.toggle_orientation)
        self.orientation_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(control_frame, text="Placez vos navires")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Frame des plateaux
        boards_frame = tk.Frame(self.window)
        boards_frame.pack(pady=10)
        
        # Plateau joueur
        player_frame = tk.Frame(boards_frame)
        player_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(player_frame, text="Votre plateau").pack()
        
        player_grid = tk.Frame(player_frame)
        player_grid.pack()
        
        # Plateau ordinateur
        computer_frame = tk.Frame(boards_frame)
        computer_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(computer_frame, text="Plateau ordinateur").pack()
        
        computer_grid = tk.Frame(computer_frame)
        computer_grid.pack()
        
        # Création des boutons des grilles
        self.player_buttons = []
        self.computer_buttons = []
        
        for i in range(10):
            row_p = []
            row_c = []
            for j in range(10):
                # Boutons joueur
                btn_p = tk.Button(player_grid, width=2, height=1, bg="white",
                                command=lambda x=i, y=j: self.player_grid_click(x, y))
                btn_p.grid(row=i, column=j)
                row_p.append(btn_p)
                
                # Boutons ordinateur
                btn_c = tk.Button(computer_grid, width=2, height=1, bg="white",
                                command=lambda x=i, y=j: self.computer_grid_click(x, y))
                btn_c.grid(row=i, column=j)
                row_c.append(btn_c)
                
            self.player_buttons.append(row_p)
            self.computer_buttons.append(row_c)

    def toggle_orientation(self):
        self.current_orientation = not self.current_orientation
        self.orientation_btn.config(text=f"Orientation: {'Horizontale' if self.current_orientation else 'Verticale'}")
    
    def player_grid_click(self, x: int, y: int):
        if not self.game_started and self.ships_to_place:
            ship_name, ship_size = self.ships_to_place[0]
            ship = Ship(ship_name, ship_size)
            
            if self.player_board.place_ship(ship, (x, y), self.current_orientation):
                self.ships_to_place.pop(0)
                self.update_player_grid()
                
                if not self.ships_to_place:
                    self.place_computer_ships()
                    self.game_started = True
                    self.status_label.config(text="À vous de jouer!")
    
    def computer_grid_click(self, x: int, y: int):
        if self.game_started and self.player_turn:
            hit, ship = self.computer_board.receive_attack((x, y))
            self.update_computer_grid()
            
            if ship and ship.is_sunk:
                messagebox.showinfo("Navire coulé!", f"Vous avez coulé le {ship.name}!")
            
            if self.computer_board.all_ships_sunk():
                messagebox.showinfo("Victoire!", "Vous avez gagné!")
                self.game_started = False
            else:
                self.player_turn = False
                self.status_label.config(text="Tour de l'ordinateur")
                self.window.after(1000, self.computer_turn)
    
    def computer_turn(self):
        if not self.player_turn:
            x, y = random.randrange(10), random.randrange(10)
            if self.player_board.grid[x][y] not in [CellState.HIT, CellState.MISS, CellState.SUNK]:
                hit, ship = self.player_board.receive_attack((x, y))
                self.update_player_grid()
                
                if ship and ship.is_sunk:
                    messagebox.showinfo("Navire coulé!", f"L'ordinateur a coulé votre {ship.name}!")
                
                if self.player_board.all_ships_sunk():
                    messagebox.showinfo("Défaite!", "L'ordinateur a gagné!")
                    self.game_started = False
                else:
                    self.player_turn = True
                    self.status_label.config(text="À vous de jouer!")
    
    def place_computer_ships(self):
        for ship_name, ship_size in self.ship_types:
            ship = Ship(ship_name, ship_size)
            placed = False
            while not placed:
                x, y = random.randrange(10), random.randrange(10)
                horizontal = random.choice([True, False])
                placed = self.computer_board.place_ship(ship, (x, y), horizontal)
    
    def update_player_grid(self):
        for i in range(10):
            for j in range(10):
                self.player_buttons[i][j].config(bg=self.player_board.grid[i][j].value)
    
    def update_computer_grid(self):
        for i in range(10):
            for j in range(10):
                if self.computer_board.grid[i][j] in [CellState.HIT, CellState.MISS, CellState.SUNK]:
                    self.computer_buttons[i][j].config(bg=self.computer_board.grid[i][j].value)
    
    def start_new_game(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.game_started = False
        self.player_turn = True
        self.ships_to_place = self.ship_types.copy()
        
        for i in range(10):
            for j in range(10):
                self.player_buttons[i][j].config(bg="white")
                self.computer_buttons[i][j].config(bg="white")
        
        self.status_label.config(text="Placez vos navires")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = BattleshipGame()
    game.run()
