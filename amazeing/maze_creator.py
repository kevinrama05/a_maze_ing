from amazeing.config_parser import ConfigParser, ConfigurationDictionary
from sys import exit
from amazeing.maze_generator import MazeGenerator
from amazeing.pathfinding import MazeSolver
import sys

# Objects:
mazegen = MazeGenerator()
config = ConfigParser()
if len(sys.argv) != 2:
    exit("Usage: python3 a_maze_ing.py <config_file>")
else:
    content = sys.argv[1]
pathfinder = MazeSolver()


def maze_creator() -> None:
    """
    The purpose of this function is to initialize, create and
    solve the maze, and save the maze, entry, exit and path on
    the OUTPUT_FILE, where each cell on the maze is represented
    by a hexadecimal value

    Args:
        None

    Returns:
        None
    """
    data: ConfigurationDictionary = config.get_config(content)

    maze = mazegen.generate_maze(
        data["HEIGHT"],
        data["WIDTH"],
        data["SEED"],
        data["PERFECT"],
        data["ENTRY"],
        data["EXIT"],
    )

    en_x, en_y = data["ENTRY"]
    ex_x, ex_y = data["EXIT"]

    path = pathfinder.bfs(
        maze, data["ENTRY"], data["EXIT"], data["HEIGHT"], data["WIDTH"]
    )
    with open(data["OUTPUT_FILE"], "w") as f:
        for i in maze:
            for j in i:
                f.write(f"{j:X}")
            f.write("\n")
        f.write(f"\n{en_x},{en_y}")
        f.write(f"\n{ex_x},{ex_y}")
        f.write(f"\n{path}")
