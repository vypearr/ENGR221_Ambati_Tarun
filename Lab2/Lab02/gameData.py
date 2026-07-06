"""
Author: Tarun Ambati
Last updated: June 29th, 2026
Description: Stores and updates the data for the game, including
the board, player movement, food, enemies, scoring, and game-over behavior.
"""

import random

from cell import Cell
from preferences import Preferences

class GameData:
    def __init__(self):
        # The current state of the board
        self.board = [[Cell(row, col) for col in range(Preferences.NUM_COLS)] 
                                      for row in range(Preferences.NUM_ROWS)]
        
        # Whether or not the game is over
        self.gameover = False

        # The current cell containing the player
        self.player = self.board[0][0]    # Start at the top left
        self.player.become_player()

        # The number of empty cells on the board, accounting for the player cell
        self.num_empty_cells = Preferences.NUM_CELLS - 1

        # A list of cells containing food
        self.food = []
        # Number of food eaten
        self.score = 0

        # A list of cells containing enemies
        self.enemies = []


    #######################
    # Game Limits Methods #
    #######################

    def at_max_food(self) -> bool:
        """ Check whether the board already has the maximum allowed food. """
        return len(self.food) >= Preferences.MAX_FOOD
    
    def at_max_enemies(self) -> bool:
        """ Check whether the board already has the maximum allowed enemies. """
        return len(self.enemies) >= Preferences.MAX_ENEMIES

    def set_game_over(self) -> None:
        """ Turn on the game over flag """
        self.gameover = True


    ##############################
    # Neighbor Retrieval Methods #
    ##############################

    def get_west_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately to the left of the given cell. 
            If we are at the  edge of the map, return None. """
        if cell.get_col() == 0:
            return None
        return self.board[cell.get_row()][cell.get_col() - 1]
        
    def get_east_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately to the right of the given cell.
            If we are at the edge of the map, return None. """
        if cell.get_col() == Preferences.NUM_COLS - 1:
            return None
        return self.board[cell.get_row()][cell.get_col() + 1]
    
    def get_north_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately above the given cell.
            If we are at the edge of the map, return None. """
        if cell.get_row() == 0:
            return None
        return self.board[cell.get_row() - 1][cell.get_col()]
        
    def get_south_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately below the given cell.
            If we are at the edge of the map, return None. """
        if cell.get_row() == Preferences.NUM_ROWS - 1:
            return None
        return self.board[cell.get_row() + 1][cell.get_col()]


    ###########################
    # Player Movement Methods #
    ###########################
        
    def move_player_right(self) -> None:
        """ Move the player one cell to the right if possible. """
        neighbor = self.get_east_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)

    def move_player_left(self) -> None:
        """ Move the player one cell to the left if possible. """
        neighbor = self.get_west_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)

    def move_player_up(self) -> None:
        """ Move the player one cell up if possible. """
        neighbor = self.get_north_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)

    def move_player_down(self) -> None:
        """ Move the player one cell down if possible. """
        neighbor = self.get_south_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)

    def move_player_to_cell(self, cell: Cell) -> None:
        """ Move the player to the given cell """

        # If there is food in this cell, eat it
        if cell.is_food():
            self.eat_food(cell)
            self.update_player_cell(cell)
        # If there is an enemy in this cell, game over!
        elif cell.is_enemy():
            self.player.become_empty()
            self.num_empty_cells += 1
            self.set_game_over()
        # Otherwise, update the player location
        else:
            self.update_player_cell(cell)

    def update_player_cell(self, new_cell: Cell) -> None:
        """ Move the player to the new cell """
    
        # Empty the cell the player just moved away from
        self.player.become_empty()
        # Update the player to the new cell
        self.player = new_cell
        # Change the new cell to be the player type
        self.player.become_player()


    ########################
    # Food Related Methods #
    ########################

    def add_food(self) -> None:
        """ Adds food to a random open spot on the board """

        # Find a row on the board
        row = random.randrange(0, Preferences.NUM_ROWS)
        # Find a col on the board
        col = random.randrange(0, Preferences.NUM_COLS)

        cell = self.board[row][col]

        # If the random cell is occupied, pick from the open cells instead.
        if not cell.is_empty():
            empty_cells = [cell for row in self.board for cell in row if cell.is_empty()]
            if not empty_cells:
                return
            cell = random.choice(empty_cells)

        cell.become_food()
        self.food.append(cell)
        self.num_empty_cells -= 1

    def eat_food(self, cell: Cell) -> None:
        """ Remove food from a cell and increase the player's score. """
        if cell in self.food:
            self.food.remove(cell)
        self.score += 1
        self.num_empty_cells += 1


    ##########################
    # Enemy Movement Methods #
    ##########################

    def add_enemy(self) -> None:
        """ Add an enemy to the bottom-right corner of the board. """
        cell = self.board[Preferences.NUM_ROWS - 1][Preferences.NUM_COLS - 1]

        # Do not stack enemies on top of each other.
        if cell.is_enemy():
            return

        if cell.is_empty():
            self.num_empty_cells -= 1
        elif cell.is_food() and cell in self.food:
            self.food.remove(cell)
        elif cell.is_player():
            self.set_game_over()

        cell.become_enemy()
        self.enemies.append(cell)

    def move_enemy_to_cell(self, enemy_cell: Cell, 
                           cell: Cell, idx: int) -> None:
        """ Move the enemy at index idx to the given destination cell. """
        if cell is None or cell.is_enemy():
            return

        if cell.is_player():
            enemy_cell.become_empty()
            self.num_empty_cells += 1
            self.set_game_over()
            return

        if cell.is_food() and cell in self.food:
            self.food.remove(cell)
        elif cell.is_empty():
            self.num_empty_cells -= 1

        enemy_cell.become_empty()
        self.num_empty_cells += 1
        cell.become_enemy()
        self.enemies[idx] = cell

    def move_enemy_left(self, idx: int) -> None:
        """ Move the enemy at index idx left one cell if possible. """
        enemy_cell = self.enemies[idx]
        self.move_enemy_to_cell(enemy_cell, self.get_west_neighbor(enemy_cell), idx)

    def move_enemy_right(self, idx: int) -> None:
        """ Move the enemy at index idx right one cell if possible. """
        enemy_cell = self.enemies[idx]
        self.move_enemy_to_cell(enemy_cell, self.get_east_neighbor(enemy_cell), idx)

    def move_enemy_up(self, idx: int) -> None:
        """ Move the enemy at index idx up one cell if possible. """
        enemy_cell = self.enemies[idx]
        self.move_enemy_to_cell(enemy_cell, self.get_north_neighbor(enemy_cell), idx)

    def move_enemy_down(self, idx: int) -> None:
        """ Move the enemy at index idx down one cell if possible. """
        enemy_cell = self.enemies[idx]
        self.move_enemy_to_cell(enemy_cell, self.get_south_neighbor(enemy_cell), idx)



if __name__ == "__main__":
    gd = GameData()
    # You can modify the line below for testing!
    print(gd.get_west_neighbor(gd.player))