import heapq
from abc import ABC, abstractmethod


class EventHandler:
    global_time = 0.0
    event_queue = []

    @classmethod
    def add_event(cls, event):
        heapq.heappush(cls.event_queue, event)

    @classmethod
    def handle_next_event(cls):
        if not cls.event_queue:
            return False, None

        event = heapq.heappop(cls.event_queue)
        cls.global_time = event.event_time
        event.execute()
        return True, event

    @classmethod
    def peek_event(cls):
        if not cls.event_queue:
            return None
        return cls.event_queue[0]


class Event(ABC):
    def __init__(self, event_time, model):
        self.event_time = event_time
        self.model = model

    def __lt__(self, other):
        return self.event_time < other.event_time

    @abstractmethod
    def execute(self):
        ...


class CellUpdateEvent(Event):
    def __init__(self, event_time, model, x, y):
        super().__init__(event_time, model)
        self.x = x
        self.y = y

    def execute(self):
        if not self.model.current_grid[self.x][self.y] == 1:
            self.model.view_grid[self.x][self.y] = 2

        self.model.handle_cell(self.x, self.y)


class GridUpdateEvent(Event):
    def execute(self):
        self.model.update_grid()


class IterationEvent(Event):
    def execute(self):
        for x in range(self.model.width):
            for y in range(self.model.height):
                EventHandler.add_event(CellUpdateEvent(self.event_time, self.model, x, y))

        EventHandler.add_event(GridUpdateEvent(self.event_time + 0.0001, self.model))
        EventHandler.add_event(IterationEvent(self.event_time + 1, self.model))
