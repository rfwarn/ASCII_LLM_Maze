class Maze:

    def __init__(self, maze_map, show_moves=True, show_coords=True, incremental_map=False, show_path_history=False, print_path_history=True, grid_list=False):
        # The map set in main. Should have a starting point and ending point and be boxed in with "#" as walls.
        self.maze_map = Maze.maps[maze_map]
        # Shows the available directions of movement for each step.
        self.show_moves = show_moves
        # Shows the coordinates of hte current position.
        self.show_coords = show_coords
        # gradually shows the map the further the user explores.
        # Not implemented yet
        self.incremental_map = incremental_map
        # Show a representation on the map of where the user has been.
        # Not implemented yet
        self.show_path_history = show_path_history
        # Records the user's valid directional moves and will be included after every move if enabled.
        self.print_path_history = print_path_history
        # Will create a 3x3 grid in a nexted list if set to true, otherwise it will be multiline text.
        self.grid_list = grid_list
        # Total move counter. Displayed when finishing maze.
        self.moves = 0
        # Total invalid move counter. Displayed when finishing maze.
        self.invalidMoves = 0
        # History of moves
        self.move_history = []
        self.start_position = self.get_pos('S')
        self.end_position = self.get_pos('E')
        self.current_position = self.start_position
        self.output = """ You have your starting position 'S', the end position 'E' and your current position will be indicated after every move with '*'.
        Walls are labeled as '#' and are impenetrable. This is done one turn at a time giving me the direction you would like to go
        (up 'U', down 'D', left 'L', right 'R'). You can also request a 3x3 grid of the immediate area around you with '3'.\n"""
        # print("You have your starting position 'S', the end position 'E' and your current position will be indicated after every move with '*'. "
        #     "Walls are labeled as '#' and are impenetrable. This is done one turn at a time giving me the direction you would like to go "
        #     "(up 'U', down 'D', left 'L', right 'R'). You can also request a 3x3 grid of the immediate area around you with '3'.")

    def get_pos(self, chr):
    # returns row, column
        for col, row in enumerate(self.maze_map):
            pos = row.find(chr)
            if pos != -1:
                return (col, pos)

    def is_valid_move(self, position):
        x, y = position
        return 0 <= x < len(self.maze_map) and 0 <= y < len(self.maze_map[0]) and self.maze_map[x][y] != '#'

    def get_valid_moves(self):
        x, y = self.current_position
        valid_moves = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_position = (x + dx, y + dy)
            if self.is_valid_move(new_position):
                valid_moves.append(new_position)
        return valid_moves

    def get_valid_openings(self):
        x, y = self.current_position
        valid_moves = []
        for direction, (dx, dy) in {'Down': (1, 0), 'Up': (-1, 0), 'Right': (0, 1), 'Left': (0, -1)}.items():
            new_position = (x + dx, y + dy)
            if self.is_valid_move(new_position):
                valid_moves.append(direction)
        return valid_moves

    def move_next(self, direction):
        x, y = self.current_position
        if direction == 'U':
            return (x - 1, y)
        elif direction == 'D':
            return (x + 1, y)
        elif direction == 'L':
            return (x, y - 1)
        elif direction == 'R':
            return (x, y + 1)
        elif direction == '3':
            self.print_3x3_maze()
            return 3
        else:
            self.output += f'incorrect input ("{direction}"), try again\n'
            self.move_history.pop()
            return False

    def is_solved(self):
        return self.current_position == self.end_position

    def print_3x3_maze(self):
        maze_map = self.maze_map.copy()
        x, y = self.current_position
        maze_map[x] = maze_map[x][:y] + '*' + maze_map[x][y+1:]
        maze_map = maze_map[x-1:x+2]
        arr = []
        for r in maze_map:
            arr.append(r[y-1:y+2])
        self.output += 'Here is a 3x3 of your current position:\n'
        if self.grid_list:
            for n, row in enumerate(arr):
                arr[n] = list(arr[n])
            # print(arr)
            self.output += str(arr)
        else:
            # for row in arr:
            #     print(''.join(row))
            self.output += '\n'.join(arr) + '\n'

    def print_maze(self):
        path_history = '·' # • (bullet), ○ (open circle), or · (middle dot). Not implemented yet...
        current_pos = '*'
        maze_map = self.maze_map.copy()
        if self.moves != 0:
            x, y = self.current_position
            maze_map[x] = maze_map[x][:y] + current_pos + maze_map[x][y+1:]

        # for row in maze_map:
        #     self.output += ''.join(row) + "\n"
        self.output += '\n'.join(maze_map) + '\n'

    def print_response(self, response):
        # Combines seperate lines into one response with new line seperators for direction integration with LLMs.
        pass

    def solve(self):
        skip = False
        while not self.is_solved():
            if not skip:
                self.print_maze()
                self.moves += 1
            else:
                skip = False
            valid_moves = self.get_valid_moves()
            if self.show_moves:
                valid_openings = self.get_valid_openings()
                # print(f'Available moves are: {valid_openings}')
                # print(f'Path History: {"".join(self.move_history)}') if self.move_history and self.print_path_history else None
                self.output += f'Available moves are: {valid_openings}\n'
                self.output += f'Path History: {"".join(self.move_history)}\n' if self.move_history and self.print_path_history else ""
            if not valid_moves:
                return False
            # Reset output to blank string for next move.
            self.output += "Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): "
            yield self.output
            self.output = ""
            move = input('').upper()
            # move = input('Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): ').upper()
            self.move_history.append(move) if move != '3' else None
            move = self.move_next(move)
            if move == 3 or not move:
                skip = True
                continue

            if move not in valid_moves:
                # print('That move is invalid since there is a wall there.')
                self.output += 'That move is invalid since there is a wall there.\n'
                self.invalidMoves += 1
                self.move_history.pop()
                continue
            self.current_position = move
            if move == self.start_position:
                # print(f'Here you are (on top of the starting point{" " + str(move) if self.show_coords else ""}):') # if self.show_coords else 'Here you are (on top of the starting point):')
                self.output += f'Here you are (on top of the starting point{" " + str(move) if self.show_coords else ""}):\n' # if self.show_coords else 'Here you are (on top of the starting point):')
            elif self.is_solved():
                # print(f'Maze solved! Completed in {self.moves} moves with {self.invalidMoves} invalid moves (running into walls).')
                self.output += f'Maze solved! Completed in {self.moves} moves with {self.invalidMoves} invalid moves (running into walls).\n'
            else:
                # print(f'Here you are{" " + str(move) if self.show_coords else ""}:') # if self.show_coords else 'Here you are:')
                self.output += f'Here you are{" " + str(move) if self.show_coords else ""}:\n'  # if self.show_coords else 'Here you are:')
            # yield self.output  # Yield the output string after each move
            # self.output = ""  # Reset the output string for the next move

        return self.output

    # def main(show_moves=True, show_coords=False, incremental_map=False, show_path_history=False):
    # def maps(num):
    # Map 1. LLM (chatGPT 4 model) had an easier time.
    maps = {"maze_map1": [
        '#########',
        '#S      #',
        '# ##### #',
        '# #     #',
        '# #E# # #',
        '# # # # #',
        '# #   # #',
        '# ##### #',
        '#########',
    ],

    # Map 2. Seems like LLMs are having a lot of trouble with this one.
    "maze_map2": [
        '#########',
        '# ##### #',
        '# #   # #',
        '# #E# # #',
        '# # # #S#',
        '#     # #',
        '# ##### #',
        '#       #',
        '#########',
    ],

    # Map 3. Another one that chatGPT had trouble getting through. 
    #   The added path history and position helped significantly and experienced much less error.
    "maze_map3": [
        '#########',
        '# ###   #',
        '# #   # #',
        '# #E# # #',
        '# # # #S#',
        '# #   # #',
        '# ##### #',
        '#       #',
        '#########',
    ],

    # Map 4. New test
    #   Trying new complexities
    "maze_map4": [
        '##############',
        '# ###    #   #',
        '# #   # #### #',
        '# #E# #     S#',
        '# # # # ######',
        '# #   # #',
        '# ##### #',
        '#       #',
        '#########',
    ]}
        # return maze_map2


if __name__ == '__main__':
    maze = Maze("maze_map2", show_moves=False, show_coords=False)
    for output in maze.solve():
        print(output)
    print(maze.output)
    # main(show_moves=False, show_coords=False)
