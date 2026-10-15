*This project has been created as part of the 42 curriculum by brasolof, mramboan.*

<h1 align="center">A-Maze-ing</h1>

## I - Description

**A-Maze-ing** is a Python maze generator. From a configuration file, the
program generates a maze (perfect or not), writes it to a file in
hexadecimal format, computes the shortest path between entry and exit, and
provides an interactive, color-coded display in the terminal.

* **Main goal**

The main goal is of this project is to **learn about random (or predefined with a seed) maze generation and maze solving algorithm**.
* **Project overview**

The core generation logic (algorithm, data structure, solving) is isolated
in a standalone, reusable Python module: **`mazegen`**.

```
.
├── Magezen
|   ├── __init__.py
|   ├── mazegen.py
|   └── README.md
├── a_maze_ing.py
├── ascii_rendering.py
├── config.txt
├── Makefile
├── mazegen-1.0-py3-none-any.whl
├── pyproject.toml
├── README.md
├── setup.cfg
└── take_config.py

```
---
## II - Instructions
While running the program, we advise you to **use a full screen terminal** to properly display the rendering.

All commands available:
* **`make install`**: Installs all required packages and create a virtual environment.
* **`make run`**: Installs packages if not done yet and run the program.
* **`make debug`**: Runs the program with pdb (PythonDeBugger).
* **`make clean`**: Deletes `__pycache__`, `.mypy_cache` and `venv_test`.
* **`make lint`**: Runs `flake8` and `mypy`.
* **`make lint-strict`**: Runs `flake8` and `mypy --strict`. 
* **`make re`**: Clears and reinstalls the packages and runs the program.
* **`make all`**: Reinstalls and runs the program.

**1.<u>Repository cloning</u>**

Clone the repository:
```
git clone git@vogsphere.42antananarivo.mg:vogsphere/intra-uuid-619b0d1d-13c4-4a65-8c4c-1e984bc5d192-7611220-mramboan A-Maze-ing
```

Enter in the directory:
```
cd A-Maze-ing
```

**2.<u>Installation</u>**

Create a `venv` named `venv_test` and install all packages (`flake8`, `mypy`, `pyfiglet`, `poetry`):
```
make install
```

**3.<u>Execution</u>**

Activate the virtual environment (The venv activation is only needed to install `flake8-docstrings` with `pip install flake8-docstrings`). **You can still run the program without it.**
```
source venv_test/bin/activate
```

Run the program:
```
make run
```
---
## III - Resources
### <u>Websites</u>:
* **Wikipedia**
* **geeksforgeeks**
* **W3schools**
* **Google Translate**
* **Youtube**

### <u>AI</u>:
Artificial Intelligence was used for certain tasks (mentioned below) due to the lack of time.
* **Claude**: The `AI Claude` was used to list every cases possible so that extensive tests can be realized. Also used to ask about specific things like error handling if the peer to peer couldn't answer our questions.
* **Gemini**: The `AI Gemini` was used to correct syntax errors.

---
## IV - Additional sections:

### 1.<u>Configuration file</u>:
The `config.txt` file contains `key=value` formats: **6 mandatory keys and 1 optional:**.<br>
Blank lines and lines starting with `#` are ignored.

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | Maze height | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `(x,y)` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `(x,y)` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze (`True`/`False`) | `PERFECT=True` |
| `SEED` | *(optional)* reproducibility seed | `SEED=42` |

Minimal example:
```
WIDTH=12
HEIGHT=12
ENTRY=0,0
EXIT=11, 11
OUTPUT_FILE=output.txt
PERFECT=True
SEED
```
**Notes:**
- The maze maximum width is set to **`52`** so that every full screen terminal can handle it.
- The minimal height and width are set to **`2`**.
- The minimal size for the maze to display the `42` pattern is **`(12*7)`**: **width = `12`** and **height = `7`**.


### 2.<u>Chosen algorithm</u>:
* **Maze generation algorithm:**<br>
**`DFS` (`Depth-First search`)** was the chosen algorithm.<br>
More presicely, DFS using a stack `(iterative version)` to stock the visited path.<br>
This algorithm visits the maze as far as possile until a dead end then proceeds a `backtracking` using the stack.<br>
`DFS` was choosen for its simplicity of implementation.

* **Maze resolution algorithm:**<br>
**`BFS` (Breadth-First Search)** was the chosen algorithm.<br>
More precisely, BFS using a queue `(iterative version)` to explore the maze level by level from the entry.
This algorithm visits all neighboring cells at the current depth before moving to cells at the next depth, guaranteeing the shortest path is found once the exit is reached.
BFS was choosen for its guarantee of finding the shortest path.


### 3.<u>Reusable code</u>:
The generation and solving logic is fully isolated in the `mazegen` module
(`MazeGenenrator` and `SolveMaze` classes), independent of display,
configuration parsing, or the user interface. It is packaged as an
installable `pip` module (`mazegen-*.whl` at the root of the
repository) and can be reused as-is in another project.

See `mazegen/README.md` for detailed documentation on how to use the module
(instantiation, parameters, accessing the structure and the solution).


### 4.<u>Project management</u>:
**brasolof**:
* `a_maze_ing.py` :
    * added seed management
    * redirection of the output into the `output.txt` file
    * error management to handle the output file

* `take_config.py` :
    * `config.txt` parsing
    * error management

* `mazegen.py` :
    * maze transcription algorithm in hexadecimal format
    * BFS resolution algorithm implemetation
    * implemetation of the algorithm for output rediction
    * path direction display
    * error management

* `Makefile` :
    * `Makefile` implementation assisted by another peer

* `config.txt` :
    * creation and implementation of `config.txt`

* `README.md` for the `mazegen` package

**mramboan**:
* `a_maze_ing.py` :
    * terminal cleaning management
    * maze display
    * error management

* `take_config.py` :
    * error management

* `mazegen.py` :
    * generation of the full grid
    * DFS algorithm implementation
    * generation of the '42' motif
    * imperfect mode implementation
    * management of avoidance of the formation of large empty areas

* `ascii_rendering` :
    * text and maze coloring

* `Makefile` :
    * added the make lint-strict rule and fixed make lint

* `setup.cfg` :
    * implemented the file

* creation of the `__init__.py` file in the `mazegen` package

* norm management

* `README.md` of the project


The project was finished a lot faster than excepted, in between 7 to 10 days but we took a long time just to start.<br>
During the first days, we learned text display in ASCII. Then the progression was exponential.<br>
We created quickly the algorithm to generate the grid, then the DFS and finally the BFS.<br>
Once the maze could have been displayed, dozens of tests were realized which allowed us to manage all of the errors.<br>
Error management along with configuration file parsing was the hardest part of the project.<br>
Package management was realized last with this README.md.

The team work was surprisingly good with great communication skills.<br>
We were able to count on each other to solve a problem or implement something so that the project could be finished quicker.<br>
The point that can be improved was the procrastination, because of that we started very late and lost time.<br>