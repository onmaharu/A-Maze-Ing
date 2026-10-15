# mazegen

Standalone, reusable Python module for generating and solving rectangular
mazes. Provides two classes: `MazeGenenrator` (generation) and `SolveMaze`
(generation + solving + file export).

## Installation

```bash
pip install mazegen-1.0-py3-none-any.whl
```

## Custom parameters

```python
maze = SolveMaze(
    width=20,           # >= 2, <= 52
    height=15,          # >= 2
    entry=(0, 0),        # (y, x), within grid bounds
    exit=(14, 19),        # (y, x), different from entry
    seeds=42,            # int | None — seed for reproducibility
    perfect=True,         # False => multiple possible paths (extra walls knocked down)
)
```

- `seeds`: if provided, calls `random.seed(seeds)` before generation - two
  calls with the same seed and the same dimensions produce the same maze.
- `perfect=False`: after generation, call `maze.to_imperfect(maze._maze)`
  to knock down extra walls and create loops.
- An invalid constructor call (dimensions too small/large, entry/exit out of
  bounds or identical) raises a `MazeError`.

## Accessing the generated structure

```python
maze.to_hexa()    # str: one line per row, one hex digit per cell
                   # (bit0=North, bit1=East, bit2=South, bit3=West;
                   # bit set to 1 = closed wall)
maze.to_ascii()    # str: ASCII/Unicode rendering of the maze
                   # marking entry/exit with 🚩/🏁
```

The raw internal structure is accessible via `maze._maze`
(`list[list[int]]`), but it is not the stable public API - prefer
`to_hexa()` / `to_ascii()`.

Note that this format is not necessarily identical to the output file
format produced by the main program (`a_maze_ing.py`), which appends entry,
exit, and the solution path after a blank line.

## Accessing the solution

```python
maze.solve()               # list[tuple[int, int]] | None
                            # shortest path (y, x) from entry to exit,
                            # computed via BFS; None if no path exists

maze.path_in_directions()  # list[str] — same path, expressed as "N"/"E"/"S"/"W"

maze.to_ascii(maze.solve())  # ASCII rendering with the solution path
                              # shown as arrows
```

## Exporting the maze to a file

```python
maze.to_fichier("output_maze.txt")
```
Writes the hexadecimal grid, a blank line, the entry coordinates, the exit
coordinates, then the solution path as `N`/`E`/`S`/`W` letters.
