"""
Maze generation logic using randomized depth-first search backtracking.

Maze solving and export functionality built on top of maze generation.
Defines :class:`MazeGenenrator`, which builds a rectangular maze grid,
optionally decorated with a fixed "42" pattern obstacle, and exposes
methods to generate the maze, make it imperfect (multiple paths), and
render it as ASCII art or a hexadecimal grid representation.
class:`SolveMaze`, which extends :class:`MazeGenenrator` with
a breadth-first search solver to find the shortest path between the
maze's entry and exit points, and utilities to export the maze and
its solution to a text file.
"""
from collections import deque
import random
from typing import Generator

error = "[Maze generation error]: "


class MazeError(Exception):
    """Custom exception thrown in the event of incorrect maze configuration."""

    pass


class MazeGenenrator:
    """Build and render a rectangular maze grid.

    Generates a maze using randomized depth-first search, optionally
    decorated with a fixed "42" pattern obstacle, and exposes methods
    to make it imperfect (multiple paths) and render it as ASCII art
    or a hexadecimal grid representation.
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            seeds: int | None = None,
            perfect: bool = True
            ):
        """
        Initialize the maze, validate the parameters.

        Args:
            width (int): Grid width (must be >= 2).
            height (int): Grid height (must be >= 2).
            entry (tuple[int, int]): (x, y) coordinates of the entry point.
            exit (tuple[int, int]): (x, y) coordinates of the exit point.
            seeds (int | None): optional seed for randomness reproducibility.
            perfect (bool): True for a single path,
                            False several paths.
        """
        if width < 2:
            raise MazeError(f"{error}Invalid Width, "
                            "must be greater or equal than 2.")
        elif width > 52:
            raise MazeError(f"{error}Width needs to be less or equal than 52.")
        self._width = width
        if height < 2:
            raise MazeError(f"{error}Invalid Height, "
                            "must be greater or equal than 2.")
        self._height = height

        if seeds is not None:
            random.seed(seeds)

        self._perfect = perfect

        self._motif: list[tuple[int, int]] = []
        self._pattern_skipped = False
        if width < 12 or height < 7:
            self._pattern_skipped = True
        else:
            self._motif = self.generate_motif()

        if (self.inside_maze(entry) is not True):
            raise MazeError(f"{error}The entry point is out of bound.")

        if (self.inside_maze(exit) is not True):
            raise MazeError(f"{error}The exit point is out of bound.")

        if (self.inside_motif(entry) is not True):
            raise MazeError(f"{error}"
                            "The entry point is inside the '42' pattern.")

        if (self.inside_motif(exit) is not True):
            raise MazeError(f"{error}"
                            "The exit point is inside the '42' pattern.")

        if entry == exit:
            raise MazeError(f"{error}Entry and exit cannot be in the"
                            " same place.")

        if not isinstance(entry[0], int) or not isinstance(entry[1], int):
            raise MazeError(f"{error}Entry coordinates must be ints")
        if not isinstance(exit[0], int) or not isinstance(exit[1], int):
            raise MazeError(f"{error}Exit coordinates must be ints")

        self._entry: tuple[int, int] = entry
        self._exit: tuple[int, int] = exit

    def inside_maze(self, point: tuple[int, int]) -> bool:
        """
        Check if a coordinate is valid.

        Check if a coordinate is inside the grid limits.

        Args:
            point (tuple[int, int]): coordinate to check.

        Return:
            bool: True if the coordinate is correct, False otherwise.
        """
        y, x = point
        if not (0 <= y < self._height) or not (0 <= x < self._width):
            return False
        else:
            return True

    def inside_motif(self, point: tuple[int, int]) -> bool:
        """
        Check if a coordinate is valid.

        Check if a coordinate is not inside the '42' pattern.

        Args:
            point (tuple[int, int]): coordinate to check.

        Return:
            bool: True if the coordinate is correct, False otherwise.
        """
        y, x = point
        if point in self._motif:
            return False
        else:
            return True

    def validate(self, point: tuple[int, int]) -> bool:
        """
        Check if a coordinate is valid.

        Check if a coordinate is not inside the
        pattern and inside the grid limits.

        Args:
            entry (tuple[int, int]): entry coordinate to check.
            exit (tuple[int, int]): exit coordinate to check.

        Return:
            bool: True if the coordinate is correct, False otherwise.
        """
        y, x = point
        if not self.inside_maze(point):
            return False
        elif not self.inside_motif(point):
            return False
        else:
            return True

    def generate_base(self) -> list[list[int]]:
        """
        Generate the starting grid filled with walls.

        Each cell is worth 15 or 1111 in binary

        Return:
            list[list[int]]: a full 2D array
        """
        base: list[list[int]] = []
        for _ in range(self._height):
            line: list[int] = []
            for _ in range(self._width):
                line.append(15)
            base.append(line)
        return base

    def generate_motif(self) -> list[tuple[int, int]]:
        """
        Calculate the "42" pattern coordinates.

        Place it in the center of the grid.

        Return:
            list[tuple[int, int]]: list of coordinates occupied by the
            obstacle.
        """
        motif: list[tuple[int, int]] = []
        yc = self._height // 2
        xc = self._width // 2
        motif.append((yc - 2, xc - 3))
        motif.append((yc - 1, xc - 3))
        motif.append((yc, xc - 3))
        motif.append((yc, xc - 2))
        motif.append((yc, xc - 1))
        motif.append((yc + 1, xc - 1))
        motif.append((yc + 2, xc - 1))

        motif.append((yc - 2, xc + 1))
        motif.append((yc - 2, xc + 2))
        motif.append((yc - 2, xc + 3))
        motif.append((yc - 1, xc + 3))
        motif.append((yc, xc + 1))
        motif.append((yc, xc + 2))
        motif.append((yc, xc + 3))
        motif.append((yc + 1, xc + 1))
        motif.append((yc + 2, xc + 1))
        motif.append((yc + 2, xc + 2))
        motif.append((yc + 2, xc + 3))
        return motif

    def open_wall(
            self,
            point: tuple[int, int],
            base: list[list[int]],
            direction: str
            ) -> None:
        """
        Break walls depending on the direction to go.

        Args:
            point (tuple[int, int]): coordinates of the current position.
            base (list[list[int]]): the grid in which to open walls.
            direction (str): direction that indicates the side of the cell
             to be removed.
        """
        west = 7
        south = 11
        east = 13
        north = 14
        y, x = point
        if direction == "W":
            base[y][x] &= west
            base[y][x - 1] &= east
        elif direction == "S":
            base[y][x] &= south
            base[y + 1][x] &= north
        elif direction == "E":
            base[y][x] &= east
            base[y][x + 1] &= west
        elif direction == "N":
            base[y][x] &= north
            base[y - 1][x] &= south

    def _is_fully_open(self, base: list[list[int]], top: int,
                       left: int, h: int, w: int) -> bool:
        """
        Check whether a rectangular window is entirely wall-free.

        Args:
            base (list[list[int]]): the grid to inspect.
            top (int): row index of the window's top-left corner.
            left (int): column index of the window's top-left corner.
            h (int): window height, in cells.
            w (int): window width, in cells.

        Return:
            bool: True if no internal wall remains in the window,
            False otherwise.
        """
        for r in range(top, top + h):
            for c in range(left, left + w - 1):
                if base[r][c] & 2:
                    return False

        for c in range(left, left + w):
            for r in range(top, top + h - 1):
                if base[r][c] & 4:
                    return False
        return True

    def _creates_forbidden_room(self, base: list[list[int]],
                                y: int, x: int) -> bool:
        """
        Check if a 3x3, 2x4, or 4x2 open room covers cell (y, x).

        Args:
            base (list[list[int]]): the grid to inspect.
            y (int): row index of the cell to check around.
            x (int): column index of the cell to check around.

        Return:
            bool: True if such a fully open room is found, False
            otherwise.
        """
        for h, w in ((3, 3), (2, 4), (4, 2)):
            for top in range(y - h + 1, y + 1):
                for left in range(x - w + 1, x + 1):
                    if top < 0 or left < 0:
                        continue
                    if top + h > self._height or left + w > self._width:
                        continue
                    if self._is_fully_open(base, top, left, h, w):
                        return True
        return False

    def to_imperfect(self, base: list[list[int]]) -> None:
        """
        Create several paths by randomly breaking additional walls.

        Each candidate wall is broken then re-checked with
        :meth:`_creates_forbidden_room`; if it would form a 3x3,
        2x4, or 4x2 open room, the break is reverted and another
        direction is tried instead. This keeps the maze imperfect
        while avoiding open rooms larger than 2x3 or 3x2.

        Args:
            base (list[list[int, int]]): reference to the grid to be made
              imperfect.
        """
        if self._height == 2 and self._width == 2:
            if (base[0][0] & 2 != 0):
                self.open_wall((0, 0), base, "E")
            if (base[0][0] & 4 != 0):
                self.open_wall((0, 0), base, "S")
        else:
            for _ in range(self._height):
                y = random.randint(0, self._height - 1)
                x = random.randint(0, self._width - 1)
                if (y, x) in self._motif:
                    continue
                directions: list[str] = []
                if (base[y][x] & 1 != 0) and self.validate((y - 1, x)):
                    directions.append("N")
                if (base[y][x] & 2 != 0) and self.validate((y, x + 1)):
                    directions.append("E")
                if (base[y][x] & 4 != 0) and self.validate((y + 1, x)):
                    directions.append("S")
                if (base[y][x] & 8 != 0) and self.validate((y, x - 1)):
                    directions.append("W")

                random.shuffle(directions)
                offsets = {"N": (-1, 0), "S": (1, 0),
                           "E": (0, 1), "W": (0, -1)}

                for direction in directions:
                    dy, dx = offsets[direction]
                    ny, nx = y + dy, x + dx

                    old_cur = base[y][x]
                    old_nb = base[ny][nx]
                    self.open_wall((y, x), base, direction)

                    if (self._creates_forbidden_room(base, y, x)
                            or self._creates_forbidden_room(base, ny, nx)):
                        base[y][x] = old_cur
                        base[ny][nx] = old_nb
                        continue
                    break

    def generate(self) -> Generator[tuple[int, int], None, None]:
        """
        Generate a maze using the DFS (Randomized Backtracker).

        Return:
            list[list[int]]: The final generated gird.
        """
        base: list[list[int]] = self.generate_base()
        visited: set[tuple[int, int]] = set()
        path: list[tuple[int, int]] = []
        path.append((0, 0))
        visited.add((0, 0))
        while path:
            y, x = path[-1]
            choices: list[tuple[int, int, str]] = []
            if self.validate((y + 1, x)) and (y + 1, x) not in visited:
                choices.append((y + 1, x, "S"))
            if self.validate((y - 1, x)) and (y - 1, x) not in visited:
                choices.append((y - 1, x, "N"))
            if self.validate((y, x + 1)) and (y, x + 1) not in visited:
                choices.append((y, x + 1, "E"))
            if self.validate((y, x - 1)) and (y, x - 1) not in visited:
                choices.append((y, x - 1, "W"))
            if choices:
                new_y, new_x, d = random.choice(choices)
                self.open_wall((y, x), base, d)
                visited.add((new_y, new_x))
                path.append((new_y, new_x))
            else:
                path.pop()
            self._maze = [row[:] for row in base]
            yield (y, x)

    def to_hexa(self) -> str:
        """
        Render the maze grid as a hexadecimal string representation.

        Each cell's 4-bit wall bitmask is converted to a single
        hexadecimal digit (0-F), with rows separated by newlines.

        Returns:
            str: The maze grid encoded as hexadecimal digits.
        """
        content = ""
        base = "0123456789ABCDEF"
        for j in range(self._height):
            for i in range(self._width):
                box = self._maze[j][i]
                content += base[box]
            content += '\n'
        return content

    def to_ascii(self, path: list[tuple[int, int]] | None = None) -> str:
        """
        Render the maze as a multi-line ASCII/Unicode art string.

        Draws walls as solid blocks and empty spaces as blank cells,
        marking the entry and exit points with flag emoji. If a path
        is provided, directional arrows are drawn along it to show
        the route from entry to exit.

        Args:
            path (list[tuple[int, int]] | None): Ordered list of
                ``(y, x)`` coordinates representing the solved path,
                used to draw directional arrows. If ``None``, no path
                is drawn.

        Returns:
            str: The maze rendered as a printable ASCII/Unicode string.
        """
        if path is None:
            path = []

        CORNER = "██"
        WALL = "██"
        WALL_V = "██"
        EMPTY = "  "
        EMPTY_V = "  "

        DIR_ARROWS = {
            (0, 1): " ▶",
            (0, -1): "◀ ",
            (1, 0): "▼ ",
            (-1, 0): "▲ ",
            }
        arrow_at = {}
        for i in range(len(path) - 1):
            y1, x1 = path[i]
            y2, x2 = path[i + 1]
            dy, dx = y2 - y1, x2 - x1
            arrow_at[(y1, x1)] = DIR_ARROWS.get((dy, dx), "??")

        result = ""
        for y in range(self._height):
            top_line = ""
            mid_line = ""
            for x in range(self._width):
                cell = self._maze[y][x]
                north = cell & 1
                west = cell & 8

                top_line += CORNER + (WALL if north else EMPTY)

                if (y, x) == self._entry:
                    content = "🚩"
                elif (y, x) == self._exit:
                    content = "🏁"
                elif (y, x) in self._motif:
                    content = "▓▓"
                elif (y, x) in arrow_at:
                    content = arrow_at[(y, x)]
                else:
                    content = "  "

                mid_line += (WALL_V if west else EMPTY_V) + content

            top_line += CORNER
            mid_line += WALL_V if (
                self._maze[y][self._width - 1] & 2) else EMPTY_V
            result += top_line + "\n" + mid_line + "\n"

        bottom_line = ""
        for x in range(self._width):
            cell = self._maze[self._height - 1][x]
            bottom_line += CORNER + (WALL if (cell & 4) else EMPTY)
        bottom_line += CORNER
        result += bottom_line + "\n"

        return result


class SolveMaze(MazeGenenrator):
    """
    A maze that can compute and export the shortest solving path.

    Extends :class:`MazeGenenrator` with pathfinding via breadth-first
    search, direction-based path representation, and file export of
    the generated maze along with its solution.
    """

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 seeds: int | None = None, perfect: bool = True):
        """Initialize the maze via the parent :class:`MazeGenenrator`."""
        super().__init__(width, height, entry, exit, seeds, perfect)

    def solve(self) -> list[tuple[int, int]] | None:
        """
        Find the shortest path from entry to exit using BFS.

        Explores the maze breadth-first from the entry point,
        following open walls only, until the exit is reached.

        Returns:
            list[tuple[int, int]] | None: The ordered list of
            ``(y, x)`` coordinates forming the shortest path from
            entry to exit, or ``None`` if no path exists.
        """
        file: deque[tuple[int, int]] = deque([self._entry])
        visited: set[tuple[int, int]] = {self._entry}
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        while file:
            y, x = file.popleft()
            if (y, x) == self._exit:
                path: list[tuple[int, int]] = [(y, x)]
                while path[-1] != self._entry:
                    path.append(parent[path[-1]])
                path.reverse()
                return path

            cell = self._maze[y][x]
            neighbors: list[tuple[int, int]] = []

            if cell & 1 == 0:
                neighbors.append((y - 1, x))
            if cell & 2 == 0:
                neighbors.append((y, x + 1))
            if cell & 4 == 0:
                neighbors.append((y + 1, x))
            if cell & 8 == 0:
                neighbors.append((y, x - 1))

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = (y, x)
                    file.append(neighbor)

        return None

    def path_in_directions(self) -> list[str]:
        """Convert the solved path's coordinates into cardinal directions.

        Calls :meth:`solve` internally and translates each consecutive
        coordinate pair into a single-letter direction.

        Returns:
            list[str]: The sequence of directions (``"N"``, ``"S"``,
            ``"E"``, ``"W"``) to follow from entry to exit. Empty if
            no path exists or the path has fewer than two points.
        """
        chemin = self.solve()
        if not chemin or len(chemin) < 2:
            return []

        directions = []
        for i in range(len(chemin) - 1):
            y1, x1 = chemin[i]
            y2, x2 = chemin[i + 1]
            if y2 < y1:
                directions.append("N")
            elif y2 > y1:
                directions.append("S")
            elif x2 > x1:
                directions.append("E")
            elif x2 < x1:
                directions.append("W")

        return directions

    def to_fichier(self, filename: str = "output_maze.txt") -> None:
        """
        Export the maze, its entry/exit points, and solution to a file.

        Writes the maze's hexadecimal grid representation, the entry
        and exit coordinates, and the solving path as a string of
        directions, each on its own line.

        Args:
            filename (str): Path of the file to write the maze export
                to. Defaults to ``"output_maze.txt"``.
        """
        chemin = self.path_in_directions()
        chemins = "".join(chemin) if chemin else "No path"

        with open(filename, "w") as f_new:
            f_new.write(self.to_hexa())
            f_new.write("\n")
            f_new.write(str(self._entry).strip('()'))
            f_new.write("\n")
            f_new.write(str(self._exit).strip('()'))
            f_new.write("\n")
            f_new.write(chemins)
