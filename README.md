# ASCII maze test for LLMs

## Introduction:

This project is a maze solver that uses large language models (LLMs) to walk through ASCII mazes. The solver updates its position one move at a time and lets the user know if it is an invalid move.

## Features:

- Supports ASCII mazes of any size
- Uses LLMs to generate text descriptions of the maze and the solver's current position
- Allows the user to input move directions and prints the maze with the updated position

## Usage:

**Clone the repository:**
`git clone https://github.com/your-username/maze-solver-llms.git`<br>
cd maze-solver-llms<br>
**Start the solver:**`python solver.py`<br>
Enter a move direction or type solve to let the solver solve the maze automatically.

**Example:**

```
>>> Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): d
>>> Good, here you are:
...
>>> Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): l
>>> That move is invalid since there is a wall there.
...
>>> Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): 3
>>> Here is a 3x3 of your current position:
>>> # #
>>> #*#
>>> # #
```

## Contributing:

If you would like to contribute to this project, please feel free to fork the repository and create a pull request. We welcome any contributions that improve the solver or make it more user-friendly.

