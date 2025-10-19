import importlib
import os
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")

# Installs needed library if not installed
def import_package(package_name):
    try:
        return importlib.import_module(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return importlib.import_module(package_name)

class ConnectFour:
    
    class Player:
        def __init__(self, id: str, disc: str):
            self.id = id
            self.disc = disc
    
    # class Player:  # Modify Player so I can use smaller data in grid
    #     def __init__(self, disc_id: int, name: str, repr: str):
    #         self.disc = disc_id
    #         self.name = name
    #         self.repr = repr

    # Grid settings
    ROWS        = 6
    COLUMNS     = 7
    SPACING     = '  '  # '  ' if os.name == 'nt' else ' '
    
    # Terminal color codes to modify text output
    __WHITE     = "\033[0m"
    __GRAY      = "\033[30m"
    __RED       = "\033[31m"
    __YELLOW    = "\033[33m"
    
    # Slot status using unicode symbols
    __FILLED    = "\u25CF"  # ◯
    __HOLLOW    = "\u25EF"  # ●
    
    # Adding color to visuals
    __SLOT      = f"{__GRAY}{__HOLLOW}{__WHITE}"    #   Gray ◯ symbol
    R_DISC      = f"{__RED}{__FILLED}{__WHITE}"     #    Red ● symbol
    Y_DISC      = f"{__YELLOW}{__FILLED}{__WHITE}"  # Yellow ● symbol
    HOW_TO_PLAY = "Press '0' to stop the game\nDrop your disc using numbers (1-7)"
    
    # Valid inputs
    VALID_KEYS  = list("01234567")

    def __init__(self):
        self.__grid       = [
            [self.__SLOT for _ in range(self.COLUMNS)] for _ in range(self.ROWS)
        ]
        self.__LABELS      = [f'{self.__WHITE}{i+1}' for i in range(self.COLUMNS)]
        self.PLAYER1       = self.Player("Red"   , self.R_DISC)
        self.PLAYER2       = self.Player("Yellow", self.Y_DISC)
        self.__running     = False
        self.__free_slots  = dict.fromkeys(range(7), 0)
        self.__end_message = ''

    def __pad(self, row):
        return self.SPACING.join(row)
    
    def display_grid(self):
        for i in map(self.__pad, self.__grid[::-1]):
            print(i)

    def __show_input_prompt(self):
        print(f"\n{self.__WHITE}{self.__pad(self.__LABELS)} : ", end='', flush=True)
    
    def __slot_available(self, column):
        row = self.__free_slots[column]
        return row < self.ROWS
    
    def __drop_disc(self, column, row):
        print(row, column)
        self.__grid[row][column] = self.__current_player.disc
        self.__free_slots[column] += 1

    def __check_victory(self, column, row):
        goal = self.__current_player.disc*4
        
        horizontal = ('{}'*self.ROWS).format(*self.__grid[row]).find(goal)
        
        items = [self.__grid[i][column] for i in range(self.ROWS)]
        vertical   = ('{}'*self.ROWS).format(*items).find(goal)

        c_d = row + column
        descending = ''.join([self.__grid[i][-i+c_d] for i in range(self.ROWS) \
                      if 0 <= -i+c_d < self.COLUMNS]).find(goal)
        
        c_a = column - row
        ascending  = ''.join([self.__grid[i][i+c_a] for i in range(self.ROWS) \
                      if 0 <= i+c_a < self.COLUMNS]).find(goal)
        
        if horizontal > -1 or vertical > -1 or descending > -1 or ascending > -1:
            id, disc = self.__current_player.id, self.__current_player.disc
            self.__end_game(f"{disc} {id} won the game! {disc}")
    
    def __full_grid(self):
        return sum(map((self.ROWS).__le__, self.__free_slots.values()))==self.COLUMNS
    
    def __switch_player(self):
        self.__current_player, self.__next_player = \
            self.__next_player, self.__current_player

    def __end_game(self, message):
        self.__running     = False
        self.__end_message = message
    
    def play(self):
        self.__running        = True
        self.__current_player = self.PLAYER1
        self.__next_player    = self.PLAYER2
        print(f'{self.__GRAY}{self.HOW_TO_PLAY}\n')
        while self.__running:
            id, disc = self.__current_player.id, self.__current_player.disc
            print(f"{self.__WHITE}{disc} {id}'s turn\n", flush=True)
            self.display_grid()
            self.__show_input_prompt()
            
            key = readchar.readkey()
            if key in self.VALID_KEYS:
                if key == '0':
                    self.__end_game("Game finished, no player won")
                else:
                    column = int(key) - 1
                    row    = self.__free_slots[column]
                    
                    if self.__slot_available(column):
                        self.__drop_disc(column, row)
                        self.__check_victory(column, row)
                        
                        if self.__full_grid():
                            self.__end_game(f"{self.R_DISC} Draw {self.Y_DISC}")
                        
                        self.__switch_player()
            
            os.system('cls' if os.name == 'nt' else 'clear')

        print()
        self.display_grid()
        print(f'\n{self.__end_message}')

if __name__ == "__main__":
    readchar = import_package("readchar")
    game = ConnectFour()
    game.play()
