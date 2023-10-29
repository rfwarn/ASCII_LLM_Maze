# ASCII Maze Solver with LLMs

## Overview:

Welcome to the ASCII maze solver - an innovative platform designed to challenge the problem-solving abilities of Large Language Models (LLMs). With this solver, users can manually navigate through ASCII-based mazes while leveraging LLMs' proficiency in dissecting problems into smaller, more manageable components. This aids in logical navigation and highlights the potential of LLMs in complex reasoning tasks.

## Key Features:

- Universal Compatibility: Accommodate ASCII mazes of various sizes.
- Maze Visualization for LLMs: After every move, the solver produces a comprehensive map displaying the absolute position. This visualization aids in providing precise feedback to Large Language Models and enhances their problem-solving capabilities.
- Interactive Navigation: Seamlessly input move directions, with the solver offering real-time updates on your current position in the maze.
- Move Validations: Receive immediate feedback on the legitimacy of your move, ensuring a guided experience.

## Getting Started:

**Clone the repository:**
`git clone https://github.com/rfwarn/ASCII_LLM_Maze.git`<br>
**Start the solver:** `python ASCIImaze.py`<br>
**Dive into the Challenge:** Provide your move direction. Inputs are flexible and not case-sensitive for user convenience.

**Example:**

```
>>> Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): d
>>> Good, here you are:
...
>>> Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): l
>>> That move is invalid since there is a wall there.
>>> Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): 3
>>> Here is a 3x3 of your current position:
>>> # #
>>> #*#
>>> # #
```

## Contributing:

If you would like to contribute to this project, please feel free to fork the repository and create a pull request. We welcome any contributions that improve the solver or make it more user-friendly.

