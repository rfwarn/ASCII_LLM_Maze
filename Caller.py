import ASCIImaze

# Create the maze object.
# maze_map2 is a string that represents the maze.
# show_moves=False hides the moves made by the solver.
# show_coords=False hides the coordinates of each cell.
maze = ASCIImaze.Maze("maze_map2", show_moves=False, show_coords=False)

# Solve the maze.
# This is a generator function that yields the output to the user or LLM.
# The solver can be interrupted by pressing Ctrl+C.
for output in maze.solve():
    # Output to the user or LLM.
    print(output)
    # User or LLM input.
    maze.get_user_move(input("").upper())
# Final solved mssage.
print(maze.output)
