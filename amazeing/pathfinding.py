from collections import deque


class MazeSolver:
    """
    The MazeSolver finds the shortest path from
    entry to exit

    Attributes:
        None
    """

    def check_walls(self, current_cell: int) -> list[str]:
        """
        This method returns all the walls that are open
        in the current cell

        Args:
            current_cell (int): The current cell represented with
                                a number from 0 to 15

        Returns:
            list[str]: All the directions where the wall is open
        """
        open_walls = []
        dirs = [(1, "N"), (2, "E"), (4, "S"), (8, "W")]

        for bitmask, label in dirs:
            # if the result of "AND" operator is 0, the wall is open
            if (current_cell & bitmask) == 0:
                open_walls.append(label)

        return open_walls

    def bfs(
        self,
        maze: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        height: int,
        width: int,
    ) -> str:
        """
        This is the maze solver. It uses Breadth First Search (BFS) to
        visit all the neighbours of the current cell, and all the neighbours
        of their neighbours, until it finds the exit. Since BFS checks the
        neighbours layer by layer, when exit is found, is with 100% certanty
        that is the shortest path.

        Args:
            maze (list[list[int]]): The maze represented by a matrix of ints
            entry (tuple[int, int]): Entry of the maze
            exit (tuple[int, int]): Exit of the maze
            height (int): Height of the maze
            width (int): Width of the maze

        Returns:
            str: The path from entry to exit
        """
        # Convert (x, y) → (row, col)
        start = (entry[1], entry[0])
        end = (exit[1], exit[0])

        the_path = ""
        queue = deque([(start, "")])
        visited = {start}
        movements = {
            "N": (-1, 0),  # up one row
            "E": (0, 1),  # right one column
            "S": (1, 0),  # down one row
            "W": (0, -1),  # left one column
        }

        while queue:
            (current_row, current_col), current_path = queue.popleft()

            if (current_row, current_col) == end:
                return current_path

            cell_value = maze[current_row][current_col]
            open_walls = self.check_walls(cell_value)

            for wall in open_walls:
                row_delta, column_delta = movements[wall]
                new_row = current_row + row_delta
                new_col = current_col + column_delta
                coords = (new_row, new_col)

                if 0 <= new_row < height and 0 <= new_col < width:
                    if coords not in visited:
                        visited.add(coords)
                        queue.append(((new_row, new_col), current_path + wall))

        return the_path
