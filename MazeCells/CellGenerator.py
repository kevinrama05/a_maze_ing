from MazeCell.Cell import *
from MazeCell.ConfigParse import ConfigParse

class MazeCells:
    def __init__(self, configs: dict) -> None:
        self.configs = configs
        self.maze_cells = []

    def is_fortytwo_valid(self) -> bool:
        """
        Checks if it is possible to visually represent 42 in the maze
        """
        return configs['HEIGHT'] >= 6 and configs['WIDTH'] >= 7

    def forty_two_coordinates(self) -> list(tuple[int, int]):
        """
        Creates the coordinates of the 42 visualization, if possible
        """
        coordinates = []
        firts_x = (self.configs['HEIGHT'] - 4) / 2
        first_y = (self.configs['WIDTH'] - 5) / 2
        # Coordinates that represent 4
        coordinates.append((first_x, first_y))
        coordinates.append((first_x + 1, first_y))
        coordinates.append((first_x + 2, first_y))
        coordinates.append((first_x + 2, first_y + 1))
        coordinates.append((first_x + 3, first_y + 1))
        # Coordinates that represent 2
        coordinates.append((first_x, first_y + 3))
        coordinates.append((first_x, first_y + 4))
        coordinates.append((first_x + 1, first_y + 4))
        coordinates.append((first_x + 2, first_y + 3))
        coordinates.append((first_x + 3, first_y + 3))
        coordinates.append((first_x + 3, first_y + 4))

    def create_cells(self) -> None:
        """
        Creates a matrix of Cells.
        """
        height = self.height
        width = self.width
        forty_two = is_fortytwo_valid()
        if forty_two:
            fortytwo_coordinates = forty_two_coordinates()

