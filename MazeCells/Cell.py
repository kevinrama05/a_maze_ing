from abc import ABC, abstractmethod


class Cell:
    """
    This is the base class of all the cells in the maze
    """
    def __init__(self) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.is_visited = False

class TopLeftCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.hard_north = True
        self.hard_west = True

class TopRightCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.hard_north = True
        self.hard_east = True

class BottomRightCell(Cell):
     def __init__(self) -> None:
         super().__init__()
         self.hard_south = True
         self.hard_west = True

class BottomLeftCell(Cell):
     def __init__(self) -> None:
         super().__init__()
         self.hard_south = True
         self.hard_east = True

class UpperCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.hard_north = True

class LowerCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.hard_south = True

class LeftyCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.hard_west = True

class RightyCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.hard_east = True

class FortyTwoCell(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.is_visited = True
