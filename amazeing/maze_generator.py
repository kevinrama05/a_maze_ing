from random import seed, shuffle
from sys import setrecursionlimit
from math import log2

setrecursionlimit(100000)


class Directions:
    """Cardinal direction constants for maze wall encoding.

    Each direction is a tuple of (dx, dy, wall_bit, opposite_bit) where
    wall_bit and opposite_bit are the bitmask values for the current and
    neighboring cell walls respectively.
    """

    N = (-1, 0, 1, 4)  # 0001, opposite = 0100
    S = (1, 0, 4, 1)  # 0100, opposite = 0001
    E = (0, 1, 2, 8)  # 0010, opposite = 1000
    W = (0, -1, 8, 2)  # 1000, opposite = 0010

    DIRECTIONS = [N, S, E, W]


class MazeGenerator:
    """Generates 2D mazes using recursive depth-first search.

    Supports perfect mazes (no loops) and imperfect mazes with extra
    paths carved near entry/exit points. Optionally embeds a '42'
    pattern into the grid for mazes larger than 8x8.
    """

    def init_maze(self, height: int, width: int) -> list[list[int]]:
        """Initializes a fully closed maze grid.

        Args:
            height: Number of rows.
            width: Number of columns.

        Returns:
            list[list[int]]: 2D list of ints where every cell is
                             0b1111 (all walls intact).
        """
        maze = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(0b1111)  # fully closed
            maze.append(row)
        return maze

    def init_visited(self, height: int, width: int) -> list[list[bool]]:
        """Initializes a visited tracking grid.

        Args:
            height: Number of rows.
            width: Number of columns.

        Returns:
            list[list[bool]]: 2D list of bools, all set to False.
        """
        visited = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(False)
            visited.append(row)
        return visited

    def carve(
        self,
        maze: list[list[int]],
        x: int,
        y: int,
        nx: int,
        ny: int,
        direction: tuple[int, int, int, int],
    ) -> None:
        """Removes the wall between two adjacent cells.

        Args:
            maze: The maze grid.
            x: Row of the current cell.
            y: Column of the current cell.
            nx: Row of the neighbor cell.
            ny: Column of the neighbor cell.
            direction: Direction tuple (dx, dy, wall_bit, opposite_bit).

        Returns:
            None
        """
        dx, dy, wall, opposite = direction

        # remove wall from current cell
        maze[x][y] &= ~wall

        # remove opposite wall from neighbor cell
        maze[nx][ny] &= ~opposite

    def dfs(
        self,
        maze: list[list[int]],
        visited: list[list[bool]],
        x: int,
        y: int,
        height: int,
        width: int,
    ) -> None:
        """Recursively carves a perfect maze via depth-first search.

        Args:
            maze: The maze grid.
            visited: Grid tracking which cells have been visited.
            x: Current row.
            y: Current column.
            height: Total number of rows.
            width: Total number of columns.

        Returns:
            None
        """
        visited[x][y] = True

        dirs = Directions.DIRECTIONS[:]
        shuffle(dirs)

        for direction in dirs:  # for each tuple in the list of tuples
            dx, dy, wall, opposite = direction  # unpack

            nx = x + dx
            ny = y + dy

            if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny]:
                self.carve(maze, x, y, nx, ny, direction)
                self.dfs(maze, visited, nx, ny, height, width)

    def lsb_one(self, num: int, n: int) -> bool:
        """Checks whether the nth least significant bit of num is set.

        Args:
            num: Integer to inspect.
            n: Bit position (0-indexed from LSB).

        Returns:
            True if the nth bit is 1, False otherwise.
        """
        return ((num >> n) & int(1)) == 1

    def add_extra_paths(
        self,
        maze: list[list[int]],
        height: int,
        width: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Adds shortcuts to create an imperfect maze.

        Carves extra passages near the entry and exit, and periodically
        removes south walls in the interior for larger mazes.

        Args:
            maze: The maze grid.
            height: Total number of rows.
            width: Total number of columns.
            entry: (col, row) tuple of the entry cell.
            exit: (col, row) tuple of the exit cell.

        Returns:
            None
        """
        y, x = entry
        dirs = Directions.DIRECTIONS[:]
        for direction in dirs:
            dx, dy, wall, opposite = direction
            ny = y + dy
            nx = x + dx
            nth_bit = int(log2(wall))
            if (
                0 <= nx < height
                and 0 <= ny < width
                and self.lsb_one(maze[x][y], nth_bit)
                and maze[nx][ny] != 15
            ):
                self.carve(maze, x, y, nx, ny, direction)
                break

        y, x = exit
        dirs = Directions.DIRECTIONS[:]
        for direction in dirs:
            dx, dy, wall, opposite = direction
            ny = y + dy
            nx = x + dx
            nth_bit = int(log2(wall))
            if (
                0 <= nx < height
                and 0 <= ny < width
                and self.lsb_one(maze[x][y], nth_bit)
                and maze[nx][ny] != 15
            ):
                self.carve(maze, x, y, nx, ny, direction)
                break

        if height > 6 and width > 6:
            count = 0
            for i in range(0, height):
                for j in range(0, width):
                    if count == 6:
                        if (
                            i != height - 1
                            and maze[i][j] != 15
                            and maze[i + 1][j] != 15
                        ):
                            if maze[i][j] & 4:
                                if (
                                    j != width - 1
                                    and maze[i][j - 1] & 4
                                    and maze[i][j + 1] & 4
                                ):
                                    maze[i][j] &= ~4
                                    maze[i + 1][j] &= ~1
                        count = 0
                    else:
                        count += 1

    def enforce_borders(
            self, maze: list[list[int]], height: int, width: int) -> None:
        """Seals all outer boundary walls of the maze.

        Args:
            maze: The maze grid.
            height: Total number of rows.
            width: Total number of columns.

        Returns:
            None
        """
        N, E, S, W = 1, 2, 4, 8

        for i in range(height):
            for j in range(width):

                # top border
                if i == 0:
                    maze[i][j] |= N

                # bottom border
                if i == height - 1:
                    maze[i][j] |= S

                # left border
                if j == 0:
                    maze[i][j] |= W

                # right border
                if j == width - 1:
                    maze[i][j] |= E

    def generate_maze(
        self,
        height: int,
        width: int,
        seed_: float,
        perfect: bool,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> list[list[int]]:
        """Generates a complete maze using DFS with optional imperfections.

        Args:
            height: Number of rows.
            width: Number of columns.
            seed: Random seed for reproducibility.
            perfect: If True, skips extra path carving.
            entry: (col, row) tuple of the entry cell.
            exit: (col, row) tuple of the exit cell.

        Returns:
            The generated maze as a 2D list of wall-encoded ints.
        """
        seed(seed_)
        maze = self.init_maze(height, width)
        visited = self.init_visited(height, width)

        if height > 8 and width > 8:
            mazeutils = MazeUtils42()
            mazeutils.isolate_42(maze, visited, height, width, entry, exit)

        self.dfs(maze, visited, 0, 0, height, width)
        if not perfect:
            self.add_extra_paths(maze, height, width, entry, exit)

        self.enforce_borders(maze, height, width)

        return maze


class MazeUtils42:
    """Utilities for embedding a '42' pattern into the maze grid."""

    def isolate_42(
        self,
        maze: list[list[int]],
        visited: list[list[bool]],
        height: int,
        width: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Marks cells forming a '42' pattern as pre-visited walls.

        Computes coordinates for the digits '4' and '2' relative to the
        maze center, shifts the pattern if it collides with entry or exit,
        then seals those cells and marks them visited before DFS runs.

        Args:
            maze: The maze grid.
            visited: Grid tracking visited cells.
            height: Total number of rows.
            width: Total number of columns.
            entry: (col, row) tuple of the entry cell.
            exit: (col, row) tuple of the exit cell.

        Returns:
            None
        """
        coordinates = []
        first_x = (height - 4) // 2
        first_y = (width - 5) // 2
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
        entry_y, entry_x = entry
        exit_y, exit_x = exit
        if (
            (entry_x, entry_y) in coordinates
            or (exit_x, exit_y) in coordinates
        ):
            if width == 8 and height == 8:
                return
            else:
                i = 0
                diff = 1
                direction = 0
                while (entry_x, entry_y) in coordinates or (
                    exit_x,
                    exit_y,
                ) in coordinates:
                    if i == 2:
                        diff += 1
                        i = 0
                    if direction == 4:
                        direction = 0
                    if direction == 0:
                        coordinates = [(x + diff, y) for x, y in coordinates]
                    elif direction == 1:
                        coordinates = [(x, y + diff) for x, y in coordinates]
                    elif direction == 2:
                        coordinates = [(x - diff, y) for x, y in coordinates]
                    elif direction == 3:
                        coordinates = [(x, y - diff) for x, y in coordinates]
                    direction += 1
                    i += 1

        for coordinate in coordinates:
            x, y = coordinate
            visited[x][y] = True
            maze[x][y] = 0b1111
