import ASCIImaze

maze = ASCIImaze.Maze("maze_map2", show_moves=False, show_coords=False)
for output in maze.solve():
    # output to the user or LLM.
    print(output)
    # User or LLM input.
    maze.get_user_move(input('').upper())
# Final solved mssage.
print(maze.output)
