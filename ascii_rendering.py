"""
ANSI terminal rendering utilities for gradient-colored text and mazes.

Provides functions to render text as ASCII/Unicode art banners and
maze grids with a smooth RGB color gradient applied character by
character, using ANSI 24-bit color escape sequences.
"""
from pyfiglet import figlet_format
import random
import shutil
from typing import Any


def lerp_color(c1: Any, c2: Any, t: Any) -> tuple[int, ...]:
    """Linearly interpolate between two RGB colors.

    Args:
        c1 (tuple[int, int, int]): Starting RGB color.
        c2 (tuple[int, int, int]): Ending RGB color.
        t (float): Interpolation factor between 0.0 and 1.0, where
            0.0 returns ``c1`` and 1.0 returns ``c2``.

    Returns:
        tuple[int, int, int]: The interpolated RGB color.
    """
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def gradient_text(
        text: Any, font: Any, color_start: Any, color_end: Any
        ) -> str:
    """
    Render text as a centered, horizontally gradient-colored ASCII banner.

    Converts the given text into ASCII art using pyfiglet, then
    applies a left-to-right RGB gradient to each character and
    centers the result within the current terminal width.

    Args:
        text (str): The text to render as a banner.
        font (str): Name of the pyfiglet font to use.
        color_start (tuple[int, int, int]): RGB color at the left
            edge of the gradient.
        color_end (tuple[int, int, int]): RGB color at the right
            edge of the gradient.

    Returns:
        str: The multi-line, ANSI-colored, centered banner string.
    """
    banner = figlet_format(text, font=font, width=200)
    lines = banner.split("\n")
    width = max(len(line) for line in lines) or 1
    terminal_size = shutil.get_terminal_size().columns
    padding = max((terminal_size - width) // 2, 0)
    result = ""
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            t = i / width
            r, g, b = lerp_color(color_start, color_end, t)
            colored_line += f"\x1b[38;2;{r};{g};{b}m{char}"
        colored_line += "\x1b[0m"
        result += " " * padding + colored_line + "\n"
    return result


def gradient_maze(maze_str: Any, color_start: Any, color_end: Any) -> str:
    """
    Apply a horizontal RGB gradient to a multi-line maze string.

    Colors each character of every line with an ANSI 24-bit color
    interpolated between ``color_start`` and ``color_end`` based on
    its horizontal position.

    Args:
        maze_str (str): The maze's multi-line ASCII/Unicode
            representation to colorize.
        color_start (tuple[int, int, int]): RGB color at the left
            edge of the gradient.
        color_end (tuple[int, int, int]): RGB color at the right
            edge of the gradient.

    Returns:
        str: The maze string with ANSI color codes applied.
    """
    lines = maze_str.split("\n")
    width = max((len(line) for line in lines), default=1) or 1
    result = ""
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            t = i / width
            r, g, b = lerp_color(color_start, color_end, t)
            colored_line += f"\x1b[38;2;{r};{g};{b}m{char}"
        colored_line += "\x1b[0m"
        result += colored_line + "\n"
    return result


def color_choice() -> list[tuple[int, int, int]]:
    """
    Pick two random RGB colors from a predefined palette.

    Returns:
        list[tuple[int, int, int]]: A list of two RGB color tuples,
        randomly selected (with possible repetition) from a fixed
        set of vivid colors, intended as gradient start and end
        colors.
    """
    color_list = [
        (255, 45, 149), (0, 240, 255),
        (255, 94, 58), (147, 51, 234),
        (0, 200, 180), (168, 85, 247),
        (163, 255, 18), (255, 0, 168),
        (255, 200, 40), (75, 30, 190),
        (255, 111, 97), (0, 206, 209),
        (255, 30, 60), (30, 60, 255),
        (255, 230, 0), (219, 0, 255)
        ]
    color = random.choices(color_list, k=2)
    return color
