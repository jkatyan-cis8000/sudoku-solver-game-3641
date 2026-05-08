#!/usr/bin/env python3
"""
Classic Sudoku Puzzle Game

A 9x9 Sudoku game with:
- Random puzzle generation
- Player input for cells
- Real-time mistake checking
- Completion validation
"""

import random
import copy


class SudokuGame:
    """Main Sudoku game logic and state management."""
    
    def __init__(self):
        """Initialize a new Sudoku game."""
        self.solution = [[0] * 9 for _ in range(9)]
        self.puzzle = [[0] * 9 for _ in range(9)]
        self.player_grid = [[0] * 9 for _ in range(9)]
        self.initial_cells = set()  # Cells that cannot be changed
        self.generate_puzzle()
    
    def generate_puzzle(self):
        """Generate a new Sudoku puzzle with a unique solution."""
        # Generate a complete valid solution
        self._fill_grid(self.solution)
        
        # Copy solution to puzzle and remove digits
        self.puzzle = copy.deepcopy(self.solution)
        self._remove_digits(self.puzzle)
        
        # Initialize player grid with initial values
        self.player_grid = copy.deepcopy(self.puzzle)
        
        # Mark initial cells (non-zero cells in puzzle)
        self.initial_cells = set()
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] != 0:
                    self.initial_cells.add((r, c))
    
    def _is_valid(self, grid, row, col, num):
        """Check if placing num at (row, col) is valid.
        
        Returns False if num conflicts with other cells in the same row, column, or subgrid.
        Returns True if there are no conflicts with other cells.
        """
        # Check row for conflicts (excluding current cell)
        for c in range(9):
            if c != col and grid[row][c] == num:
                return False
        
        # Check column for conflicts (excluding current cell)
        for r in range(9):
            if r != row and grid[r][col] == num:
                return False
        
        # Check 3x3 subgrid for conflicts (excluding current cell)
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and grid[r][c] == num:
                    return False
        
        return True
    
    def _fill_grid(self, grid):
        """Fill the grid with a valid Sudoku solution using backtracking."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    # Try digits 1-9 in random order
                    digits = list(range(1, 10))
                    random.shuffle(digits)
                    
                    for num in digits:
                        if self._is_valid(grid, row, col, num):
                            grid[row][col] = num
                            
                            if self._fill_grid(grid):
                                return True
                            
                            grid[row][col] = 0
                    
                    return False
        return True
    
    def _remove_digits(self, grid, holes=45):
        """Remove digits to create a playable puzzle."""
        # Create list of all cell positions
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        # Remove the specified number of cells
        for r, c in cells[:holes]:
            grid[r][c] = 0
    
    def is_cell_initial(self, row, col):
        """Check if a cell is part of the initial puzzle."""
        return (row, col) in self.initial_cells
    
    def set_cell(self, row, col, value):
        """Set a cell's value. Returns True if valid, False if mistake."""
        if self.is_cell_initial(row, col):
            return None  # Cannot modify initial cells
        
        if value < 0 or value > 9:
            return None
        
        self.player_grid[row][col] = value
        
        # Check if this creates a conflict (only if value is non-zero)
        if value != 0 and not self._is_valid(self.player_grid, row, col, value):
            return False  # Mistake: value conflicts with existing cells
        
        return True  # Valid placement (including clearing with value 0)
    
    def check_solution(self):
        """Check if the puzzle is completed correctly."""
        # Check if grid is full
        for r in range(9):
            for c in range(9):
                if self.player_grid[r][c] == 0:
                    return False  # Grid not full
        
        # Check if the solution matches the expected solution
        return self.player_grid == self.solution
    
    def get_cell(self, row, col):
        """Get the value at a cell."""
        return self.player_grid[row][col]
    
    def get_puzzle_cell(self, row, col):
        """Get the initial value at a cell (from the puzzle)."""
        return self.puzzle[row][col]

    def display_grid(self):
        """Display the current grid state."""
        print_grid(self.puzzle, self.player_grid, self.initial_cells)


def print_grid(grid, player_grid=None, initial_cells=None):
    """Print the Sudoku grid in a readable format."""
    if player_grid is None:
        player_grid = grid
    if initial_cells is None:
        initial_cells = set()
    
    print("\n" + "=" * 25)
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("-" * 25)
        
        row_str = ""
        for col in range(9):
            if col % 3 == 0 and col != 0:
                row_str += "| "
            
            cell = player_grid[row][col]
            if cell == 0:
                row_str += ". "
            else:
                # Highlight initial cells
                if (row, col) in initial_cells:
                    row_str += f"\033[1m{cell}\033[0m "
                else:
                    row_str += f"{cell} "
        
        print(row_str)
    print("=" * 25 + "\n")


def print_help():
    """Print help information."""
    print("\n=== Controls ===")
    print("set <row> <col> <value>  - Set a cell (rows/cols: 1-9, value: 1-9)")
    print("clear <row> <col>        - Clear a cell (set to 0)")
    print("show                     - Show current grid")
    print("check                    - Check your solution")
    print("new                      - Generate a new puzzle")
    print("help                     - Show this help")
    print("quit                     - Exit the game")
    print("")


def play_game():
    """Main game loop."""
    print("\n" + "=" * 50)
    print("       WELCOME TO SUDOKU!")
    print("=" * 50)
    print("\nFill the 9x9 grid so that each row, column, and")
    print("3x3 subgrid contains all digits 1-9 exactly once.")
    print("\nInitial cells are shown in \033[1mbold\033[0m.")
    print("Type 'help' for controls.")
    
    game = SudokuGame()
    
    while True:
        print_grid(game.puzzle, game.player_grid, game.initial_cells)
        
        try:
            command = input("Enter command: ").strip().lower()
        except EOFError:
            print("\nGame ended.")
            break
        
        if not command:
            continue
        
        parts = command.split()
        cmd = parts[0]
        
        if cmd == "quit":
            print("\nThanks for playing!")
            break
        
        elif cmd == "help":
            print_help()
        
        elif cmd == "show":
            continue  # Already showing grid
        
        elif cmd == "new":
            game = SudokuGame()
            print("\nNew puzzle generated!")
        
        elif cmd == "check":
            if game.check_solution():
                print("\n\033[92m🎉 CONGRATULATIONS! You solved the puzzle!\033[0m")
            else:
                # Check for mistakes
                mistakes = []
                for r in range(9):
                    for c in range(9):
                        val = game.get_cell(r, c)
                        if val != 0 and not game._is_valid(game.player_grid, r, c, val):
                            mistakes.append((r + 1, c + 1, val))
                
                if mistakes:
                    print("\n\033[91m❌ Mistakes found:\033[0m")
                    for r, c, val in mistakes:
                        print(f"   - Cell ({r}, {c}) with value {val} conflicts")
                
                # Check if grid is full
                full = all(game.get_cell(r, c) != 0 
                          for r in range(9) for c in range(9))
                if not full:
                    print("\nThe grid is not full yet. Keep going!")
                else:
                    print("\nThe solution is incorrect. Keep trying!")
        
        elif cmd == "set" and len(parts) == 5:
            try:
                row = int(parts[1]) - 1
                col = int(parts[2]) - 1
                value = int(parts[3])
                
                if not (0 <= row < 9 and 0 <= col < 9 and 1 <= value <= 9):
                    print("\n\033[93mInvalid input! Use rows/cols 1-9 and value 1-9\033[0m")
                    continue
                
                result = game.set_cell(row, col, value)
                
                if result is None:
                    print("\n\033[93mCannot modify initial cells!\033[0m")
                elif result:
                    print(f"\n\033[92m✓ Set cell ({row+1}, {col+1}) to {value}\033[0m")
                else:
                    print(f"\n\033[91m✗ Mistake! Value {value} conflicts in row/col/subgrid\033[0m")
            
            except ValueError:
                print("\n\033[93mInvalid input! Use: set <row> <col> <value>\033[0m")
        
        elif cmd == "clear" and len(parts) == 3:
            try:
                row = int(parts[1]) - 1
                col = int(parts[2]) - 1
                
                if not (0 <= row < 9 and 0 <= col < 9):
                    print("\n\033[93mInvalid input! Use rows/cols 1-9\033[0m")
                    continue
                
                if game.is_cell_initial(row, col):
                    print("\n\033[93mCannot modify initial cells!\033[0m")
                else:
                    game.set_cell(row, col, 0)
                    print(f"\n\033[92m✓ Cleared cell ({row+1}, {col+1})\033[0m")
            
            except ValueError:
                print("\n\033[93mInvalid input! Use: clear <row> <col>\033[0m")
        
        else:
            print("\n\033[93mUnknown command! Type 'help' for controls.\033[0m")


if __name__ == "__main__":
    play_game()
