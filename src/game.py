from abc import ABC, abstractmethod
from copy import deepcopy

from events import EventHandler, IterationEvent, CellUpdateEvent, GridUpdateEvent
from utils import BLACK_SQUARE, WHITE_SQUARE, GRAY_SQUARE, clear_lines


class GameLife(ABC):
    def __init__(self, width, height, start_grid=None):
        self.width = width
        self.height = height
        self._started = False

        self.current_grid = start_grid
        if start_grid is None:
            self.current_grid = [[0] * height for _ in range(width)]
        self.next_grid = [[0] * height for _ in range(width)]

    @abstractmethod
    def get_neighbor(self, x, y, dx, dy):
        ...

    def count_neighbors(self, x, y):
        count = 0

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue

                neighbor = self.get_neighbor(x, y, dx, dy)
                if neighbor is None:
                    continue

                nx, ny = neighbor
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

    @abstractmethod
    def step(self):
        ...

    @abstractmethod
    def display(self, extra_line=False):
        ...

    def _clear_prev_grid(self, extra_line=False):
        if not self._started:
            self._started = True
        else:
            clear_lines(self.height + extra_line)


class SimpleGameLife(GameLife):
    def get_neighbor(self, x, y, dx, dy):
        nx, ny = x + dx, y + dy

        if not (0 <= nx < self.width) or not (0 <= ny < self.height):
            return None

        return nx, ny

    def step(self):
        for x in range(self.width):
            for y in range(self.height):
                self.handle_cell(x, y)

        self.update_grid()

    def display(self, extra_line=False):
        self._clear_prev_grid(extra_line)
        for row in self.current_grid:
            print("".join([BLACK_SQUARE if cell else WHITE_SQUARE for cell in row]))


class DEVSGameLife(GameLife):
    def __init__(self, width, height, start_grid=None):
        super().__init__(width, height, start_grid)
        self.view_grid = deepcopy(self.current_grid)

    def get_neighbor(self, x, y, dx, dy):
        nx, ny = (x + dx) % self.width, (y + dy) % self.height
        return nx, ny

    def update_grid(self):
        super().update_grid()
        self.view_grid = deepcopy(self.current_grid)

    def step(self):
        next_event = EventHandler.peek_event()

        if isinstance(next_event, (IterationEvent, CellUpdateEvent)):
            if isinstance(next_event, IterationEvent):
                EventHandler.handle_next_event()

            while isinstance(EventHandler.peek_event(), CellUpdateEvent):
                EventHandler.handle_next_event()

            return

        if isinstance(EventHandler.peek_event(), GridUpdateEvent):
            EventHandler.handle_next_event()
            return

    def display(self, extra_line=False):
        self._clear_prev_grid(extra_line)
        for row in self.view_grid:
            print("".join([BLACK_SQUARE if cell == 1 else GRAY_SQUARE if cell == 2 else WHITE_SQUARE for cell in row]))
