"""
Entry point for the A-Maze-Ing maze generator application.

Loads a maze configuration from a file, generates a maze, and provides
an interactive command-line interface to regenerate, display, and
customize the maze until the user chooses to quit.
"""

from ascii_rendering import gradient_text, color_choice, gradient_maze
from mazegen import MazeError, SolveMaze
import random
import sys
from take_config import load_config, ConfigurationError
from typing import Any


error = "[Maze Configuration Error]: "


def clear_screen() -> None:
    """
    Clear the terminal screen and scrollback buffer.

    Uses ANSI escape sequences to erase the visible screen, the
    scrollback buffer, and reset the cursor position to the top-left
    corner.
    """
    print("\033[2J\033[3J\033[H", end="", flush=True)


def display_maze(maze: Any, show_path: Any, colors: Any, seed: Any) -> None:
    """
    Render the maze and the interactive command menu to the terminal.

    Args:
        maze: The maze object to display, providing ``to_ascii`` and
            ``solve`` methods.
        show_path (bool): Whether to highlight the solved path from
            entry to exit.
        colors (tuple): A pair of colors used for the gradient title
            and maze rendering.
        seed (int): The random seed used to generate the current maze,
            shown to the user for reference.
    """
    print(gradient_text("A-Maze-Ing", "larry3d", colors[0], colors[1]))
    print()

    if show_path:
        path = maze.solve()
        print(gradient_maze(maze.to_ascii(path), colors[0], colors[1]))
    else:
        print(gradient_maze(maze.to_ascii(), colors[0], colors[1]))

    print(f"Seed: {seed}")

    if maze._pattern_skipped:
        print("Note: maze dimensions are too small to display the pattern.")

    print("\n=== Available commands ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")


if __name__ == "__main__":
    import os

    if len(sys.argv) == 2:
        fichier_config = sys.argv[1]

        if not os.path.exists(fichier_config):
            print(f"File error : File '{fichier_config}' not found.")
            sys.exit(1)

        try:
            config = load_config(fichier_config)

            width = config["WIDTH"]
            heigth = config["HEIGHT"]
            entry = config["ENTRY"]
            exit_point = config["EXIT"]
            is_perfect = config["PERFECT"]
            output_file = config["OUTPUT_FILE"]

            colors = color_choice()

            seed = config["SEED"]
            if seed is None:
                seed = random.randint(0, 2**31 - 1)

            maze = SolveMaze(width, heigth, entry=entry, exit=exit_point,
                             seeds=seed)

            for _ in maze.generate():
                pass

            if not is_perfect:
                maze.to_imperfect(maze._maze)

            try:
                maze.to_fichier(output_file)
            except OSError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

            show_path = False

            while True:
                clear_screen()
                display_maze(maze, show_path, colors, seed)

                user_input = input("Enter your choice: ")

                if user_input == '1':
                    if config["SEED"] is None:
                        seed = random.randint(0, 2**31 - 1)

                    new_maze = SolveMaze(width, heigth, entry=entry,
                                         exit=exit_point, seeds=seed)
                    for _ in new_maze.generate():
                        pass

                    if not is_perfect:
                        new_maze.to_imperfect(new_maze._maze)

                    new_maze.to_fichier(output_file)

                    maze = new_maze
                    show_path = False

                elif user_input == '2':
                    show_path = not show_path

                elif user_input == '3':
                    colors = color_choice()

                elif user_input == '4':
                    break

                else:
                    raise ConfigurationError(
                        "Please run the program again "
                        "and choose a number from 1 to 4."
                        )

        except KeyError as e:
            print(f"Error: {e} key is missing in config.txt file.")
        except ConfigurationError as e:
            print(f"Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram interupted by user.")
        except MazeError as e:
            print(e)
    else:
        print("The argument is missing the 'config.txt' file."
              "\nUsage: python3 a_maze_ing.py config.txt")
