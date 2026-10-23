from typing import TypedDict


class ParseDict(TypedDict):
    maze: list[str]
    entry: tuple[int, int]
    exit_: tuple[int, int]
    path: str


def parse_maze_output() -> ParseDict:
    """
    Reads the OUTPUT_FILE and converts its content in a dictionary

    Args:
        None

    Returns:
        dict[str, Union[str, tuple[int, int]]]: The maze's maze, entry, exit
                                                and path
    """
    with open("config.txt", "r") as f:
        for i in f.readlines():
            if "OUTPUT_FILE" in i:
                line = i.rstrip()
                garbage, output_file = line.split("=", 1)
                break

    with open(output_file.rstrip(), "r") as f:
        lines = [line.rstrip("\n") for line in f]

    separator = lines.index("")

    maze_hex = lines[:separator]
    entry_line, exit_line, path_line = lines[separator + 1:]

    entry_x, entry_y = entry_line.split(",", 1)
    exit_x, exit_y = exit_line.split(",", 1)
    entry = (int(entry_x), int(entry_y))
    exit_ = (int(exit_x), int(exit_y))

    return ParseDict(
        maze=maze_hex,
        entry=entry,
        exit_=exit_,
        path=path_line
    )


def change_seed(new_seed: int) -> None:
    """
    It changes the seed from the configuration file

    Args:
        new_seed (int): The new seed to add in the configuration file

    Returns:
        None
    """
    with open("config.txt", "r") as f:
        lines = f.readlines()

    with open("config.txt", "w") as f:
        for i in lines:
            if "SEED" in i or i.rstrip() == "":
                pass
            else:
                f.write(i)

    with open("config.txt", "r") as f:
        last_line = f.readlines()[-1]

    with open("config.txt", "a") as f:
        if last_line[-1] == "\n":
            f.write(f"SEED={new_seed}")
        else:
            f.write(f"\nSEED={new_seed}")
        return
