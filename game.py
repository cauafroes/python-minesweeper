import tkinter as tk
import random

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = 0

    def is_sunk(self):
        return self.hits >= self.size

class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship, x, y, horizontal):
        if horizontal:
            if y + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[x][y + i] != ' ':
                    return False
            for i in range(ship.size):
                self.grid[x][y + i] = ship
        else:
            if x + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[x + i][y] != ' ':
                    return False
            for i in range(ship.size):
                self.grid[x + i][y] = ship
        self.ships.append(ship)
        return True

    def receive_attack(self, x, y):
        if isinstance(self.grid[x][y], Ship):
            ship = self.grid[x][y]
            ship.hits += 1
            self.grid[x][y] = 'X'
            return 'Hit' if not ship.is_sunk() else f"{ship.name} sunk!"
        elif self.grid[x][y] == ' ':
            self.grid[x][y] = 'O'
            return 'Miss'
        return 'Already attacked'

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.enemy_view = [[' ' for _ in range(10)] for _ in range(10)]

    def place_ships(self):
        ships = [("Submarine", 1), ("Submarine", 1), ("Submarine", 1), ("Submarine", 1),
                 ("Destroyer", 3), ("Destroyer", 3), ("Carrier", 4)]
        for name, size in ships:
            placed = False
            while not placed:
                x, y = random.randint(0, 9), random.randint(0, 9)
                horizontal = random.choice([True, False])
                placed = self.board.place_ship(Ship(name, size), x, y, horizontal)

class NavalBattleGame:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.current_player = self.player1
        self.opponent = self.player2
        self.game_over = False

        # Place ships
        self.player1.place_ships()
        self.player2.place_ships()

        # Set up the Tkinter window
        self.window = tk.Tk()
        self.window.title("Naval Battle Game")

        # Status Label
        self.status_label = tk.Label(self.window, text=f"{self.current_player.name}'s turn", font=("Arial", 16))
        self.status_label.grid(row=0, column=0, columnspan=20)

        # Create Player 1's Board
        tk.Label(self.window, text="Player 1's Board", font=("Arial", 12)).grid(row=1, column=0, columnspan=10)
        self.player1_buttons = [[None for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                btn = tk.Button(self.window, text=" ", width=2, height=1,
                                command=lambda x=x, y=y: self.attack(x, y, self.player1))
                btn.grid(row=x + 2, column=y)
                self.player1_buttons[x][y] = btn

        # Spacer between the boards
        tk.Label(self.window, text="   ").grid(row=1, column=10)

        # Create Player 2's Board
        tk.Label(self.window, text="Player 2's Board", font=("Arial", 12)).grid(row=1, column=11, columnspan=10)
        self.player2_buttons = [[None for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                btn = tk.Button(self.window, text=" ", width=2, height=1,
                                command=lambda x=x, y=y: self.attack(x, y, self.player2))
                btn.grid(row=x + 2, column=y + 11)
                self.player2_buttons[x][y] = btn

    def attack(self, x, y, target_player):
        if self.game_over or target_player != self.opponent:
            return

        result = self.opponent.board.receive_attack(x, y)
        self.update_buttons(self.opponent, x, y, result)

        if self.opponent.board.all_ships_sunk():
            self.status_label.config(text=f"{self.current_player.name} wins!")
            self.game_over = True
            self.reveal_ships()
        else:
            # Update the attacking player's view
            self.update_attack_indicator(x, y)
            # Update the attacking board with an asterisk
            self.update_player_board_indicator(x, y)
            # Switch turns
            self.current_player, self.opponent = self.opponent, self.current_player
            self.status_label.config(text=f"{self.current_player.name}'s turn")

    def update_buttons(self, player, x, y, result):
        button = self.player1_buttons[x][y] if player == self.player2 else self.player2_buttons[x][y]
        if result == 'Hit' or 'sunk' in result:
            button.config(text="X", bg="red")
        elif result == 'Miss':
            button.config(text="O", bg="blue")

    def update_attack_indicator(self, x, y):
        """Update the button on the attacking player's board to indicate the attack."""
        button = self.player1_buttons[x][y] if self.current_player == self.player1 else self.player2_buttons[x][y]
        button.config(text="A", bg="yellow")  # Use "A" to indicate an attack

    def update_player_board_indicator(self, x, y):
        """Update the attacking player's board to show where they attacked."""
        button = self.player2_buttons[x][y] if self.current_player == self.player1 else self.player1_buttons[x][y]
        button.config(text="*", bg="lightgray")  # Indicate the attack with an asterisk

    def reveal_ships(self):
        """Reveal all remaining ships on both boards at the end of the game."""
        for x in range(10):
            for y in range(10):
                if isinstance(self.player1.board.grid[x][y], Ship):
                    self.player1_buttons[x][y].config(text="S", bg="gray")
                if isinstance(self.player2.board.grid[x][y], Ship):
                    self.player2_buttons[x][y].config(text="S", bg="gray")

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = NavalBattleGame()
    game.start()
