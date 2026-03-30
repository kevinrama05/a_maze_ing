from Cell import *
from ConfigParse import ConfigParse

class MazeCells:
    def __init__(self, configs: ConfigParse) -> None:
        self.configs = configs
        self.maze_cells = []

    def is_fortytwo_valid(self) -> bool:
        """
        Checks if it is possible to visually represent 42 in the maze
        """
        return configs.config['HEIGHT'] >= 6 and configs.config['WIDTH'] >= 7

    def forty_two_coordinates(self) -> list(tuple[int, int]):
        """
        Creates the coordinates of the 42 visualization, if possible
        """
        coordinates = []
        first_x = (self.configs.config['HEIGHT'] - 4) // 2
        first_y = (self.configs.config['WIDTH'] - 5) // 2
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
        return coordinates

    def create_cells(self) -> None:
        """
        Creates a matrix of Cells.
        """
        height = self.configs.config['HEIGHT']
        width = self.configs.config['WIDTH']
        i = 0
        j = 0
        while len(self.maze_cells) < height:
            self.maze_cells.append([])
            while len(self.maze_cells[i]) < width:
                self.maze_cells[i].append({'coordinate': (i, j), 'cell_type': None})
                j += 1
            i += 1
            j = 0

    def assign_cells(self) -> None:
        """
        Assigns the right Cell type for each cell
        """
        height = self.configs.config['HEIGHT']
        width = self.configs.config['WIDTH']
        if self.is_fortytwo_valid():
            fortytwo_coordinates = self.forty_two_coordinates()
        else:
            fortytwo_coordinates = []
        for i in self.maze_cells:
            for j in i:
                coordinate = j['coordinate']
                x, y = coordinate
                if coordinate in fortytwo_coordinates:
                    j['cell_type'] = FortyTwoCell()
                elif coordinate == (0, 0):
                    j['cell_type'] = TopLeftCell()
                elif coordinate == (0, width - 1):
                    j['cell_type'] = TopRightCell()
                elif coordinate == (height - 1, 0):
                    j['cell_type'] = BottomLeftCell()
                elif coordinate == (height - 1, width - 1):
                    j['cell_type'] = BottomRightCell()
                elif x == 0:
                    j['cell_type'] = UpperCell()
                elif x == height - 1:
                    j['cell_type'] = LowerCell()
                elif y == 0:
                    j['cell_type'] = LeftyCell()
                elif y == width - 1 :
                    j['cell_type'] = RightyCell()
                else:
                    j['cell_type'] = Cell()


if __name__ == "__main__":
    configs = ConfigParse()
    configs.read_config_file()
    configs.get_keys()
    configs.parse_keys()
    configs.validate_values()
    maze = MazeCells(configs)
    maze.create_cells()
    maze.assign_cells()
    for i in maze.maze_cells:
        for j in i:
            if isinstance(j['cell_type'], TopLeftCell):
                print("/", end="")
            elif isinstance(j['cell_type'], TopRightCell):
                print("\\", end="")
            elif isinstance(j['cell_type'], BottomLeftCell):
                print("$", end="")
            elif isinstance(j['cell_type'], BottomRightCell):
                print("%", end="")
            elif isinstance(j['cell_type'], UpperCell) or isinstance(j['cell_type'], LowerCell):
                print("-", end="")
            elif isinstance(j['cell_type'], LeftyCell) or isinstance(j['cell_type'], RightyCell):
                print("|", end="")
            elif isinstance(j['cell_type'], FortyTwoCell):
                print("H", end="")
            else:
                print("•", end="")
        print()
