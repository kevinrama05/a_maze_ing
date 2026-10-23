from amazeing.maze_creator import maze_creator


def main() -> None:
    try:
        maze_creator()
        from amazeing.mlx_gui import mlx_gui
        mlx_gui()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
