class Maze:
    def __init__(self, maze_map, show_moves):
        self.maze_map = maze_map
        self.show_moves = show_moves
        self.start_position = self.get_pos('S')
        self.end_position = self.get_pos('E')
        self.current_position = self.start_position
        print("You have your starting position 'S', the end position 'E' and your current position will be indicated after every move with '*'. " 
            "Walls are labeled as '#' and are impenetrable. This is done one turn at a time giving me the direction you would like to go "
            "(up 'U', down 'D', left 'L', right 'R'). You can also request a 3x3 grid of the immediate area around you with '3'.")
    
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
            print(f'incorrect input ("{direction}"), try again')
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
        print('Here is a 3x3 of your current position:')
        for row in arr:
            print(''.join(row))

    def print_maze(self, start=True):
        maze_map = self.maze_map.copy()
        if start:
            x, y = self.current_position
            maze_map[x] = maze_map[x][:y] + '*' + maze_map[x][y+1:]

        for row in maze_map:
            print(''.join(row))

    def solve(self):
        skip = False
        while not self.is_solved():
            if not skip:
                self.print_maze()
            else:
                skip = False
            valid_moves = self.get_valid_moves()
            if self.show_moves:
                valid_openings = self.get_valid_openings()
                print(f'Available moves are: {valid_openings}')
            if not valid_moves:
                return False
            move = input('Enter a move direction (U, D, L, R, or 3 (for a 3x3 of the current position)): ').upper()
            move = self.move_next(move)
            if move == 3:
                skip = True
                continue
            elif not move:
                skip = True
                continue
            if move not in valid_moves:
                print('That move is invalid since there is a wall there.')
                continue
            elif move == self.start_position:
                print('Here you are (on top of the starting point):')
            else:
                print('Here you are:')

            self.current_position = move

        return True


def main(show_moves=True):
    # Map 1. LLM (chatGPT 4 model) had an easier time.
    # maze_map = [
    #     '#########',
    #     '#S      #',
    #     '# ##### #',
    #     '# #     #',
    #     '# #E# # #',
    #     '# # # # #',
    #     '# #   # #',
    #     '# ##### #',
    #     '#########',
    # ]

    # Map 2. Seems like LLMs are having a lot of trouble with this one.
    maze_map = [
        '#########',
        '# ##### #',
        '# #   # #',
        '# #E# # #',
        '# # # #S#',
        '#     # #',
        '# ##### #',
        '#       #',
        '#########',
    ]

    maze = Maze(maze_map, show_moves)

    if maze.solve():
        print('Maze solved!')
    else:
        print('Maze could not be solved.')


if __name__ == '__main__':
    main(show_moves=True)