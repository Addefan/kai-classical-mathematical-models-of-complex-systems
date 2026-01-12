from utils import BLACK_SQUARE, WHITE_SQUARE, clear_lines


class SimpleGameLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.started = False

        self.current_grid = [[0] * height for _ in range(width)]
        self.next_grid = [[0] * height for _ in range(width)]

    def count_neighbors(self, x, y):
        count = 0

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.width) or not (0 <= ny < self.height):
                    continue

                if self.current_grid[nx][ny] == 1:
                    count += 1

        return count

    def handle_cell(self, x, y):
        neighbors = self.count_neighbors(x, y)
        is_alive = self.current_grid[x][y] == 1

        if is_alive and neighbors in (2, 3):
            self.next_grid[x][y] = 1
        elif not is_alive and neighbors == 3:
            self.next_grid[x][y] = 1
        else:
            self.next_grid[x][y] = 0

    def update_grid(self):
        for x in range(self.width):
            for y in range(self.height):
                self.current_grid[x][y] = self.next_grid[x][y]

    def step(self):
        for x in range(self.width):
            for y in range(self.height):
                self.handle_cell(x, y)

        self.update_grid()

    def display(self, extra_line=False):
        if not self.started:
            self.started = True
        else:
            clear_lines(self.height + extra_line)

        for row in self.current_grid:
            print("".join([BLACK_SQUARE if cell else WHITE_SQUARE for cell in row]))
