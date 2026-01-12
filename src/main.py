import time
from copy import deepcopy

from events import EventHandler, IterationEvent
from game import SimpleGameLife, DEVSGameLife


def run_game(game, delay=None):
    print("Запуск игры \"Жизнь\"...\n")

    print("Управление игрой:")
    print("• для начала игры нажмите \033[7mEnter\033[0m;")
    if not delay:
        print("• для перехода к следующему шагу нажмите \033[7mEnter\033[0m;")
    print("• для выхода из игры нажмите \033[7mCtrl+C\033[0m.\n")

    game.display()
    input("Начальное состояние ↑")

    try:
        started = False
        while True:
            game.display(extra_line=not started or not delay)
            started = True
            game.step()

            if not delay:
                input()
            else:
                time.sleep(delay)

    except KeyboardInterrupt:
        print("Игра остановлена пользователем.")


def main():
    width, height = 10, 10

    # неподвижный
    # start_grid = [[0] * height for _ in range(width)]
    # start_grid[4][4] = start_grid[4][5] = start_grid[3][4] = start_grid[3][5] = 1

    # осциллирующий
    # start_grid = [[0] * height for _ in range(width)]
    # start_grid[4][4] = start_grid[4][5] = start_grid[4][6] = 1

    # зацикленный и движущийся
    start_grid = [[0] * height for _ in range(width)]
    start_grid[8][0] = start_grid[7][1] = 1
    start_grid[7][2] = start_grid[8][2] = start_grid[9][2] = 1

    simple_game = SimpleGameLife(width, height, deepcopy(start_grid))
    devs_game = DEVSGameLife(width, height, deepcopy(start_grid))
    delay = 0.5

    run_game(simple_game, delay)
    EventHandler.add_event(IterationEvent(0, devs_game))
    run_game(devs_game, delay)


if __name__ == "__main__":
    main()
