# Бег с препятствиями - создается условная карта трассы в виде матрицы,
# ширина которой соответствует количеству бегунов, а высота – фиксирована,
# содержащей произвольное количество единиц (препятствий) в произвольных
# ячейках. Стартующие бегуны (процессы) перемещаются по трассе и при встрече
# с препятствием задерживаются на фиксированное время. По достижении
# финиша бегуны сообщают свой номер. Реализуйте соответствующие программы,
# используя механизмы процессов.


from random import random
from threading import Thread, Lock
from time import sleep

global_print_lock = Lock()

class Map:
    def __init__(self, runners_count: int, map_length: int):
        self._runners_count = runners_count
        self._map_length = map_length
        self._map = self._generate()

    @property
    def length(self) -> int:
        return self._map_length

    def get_row(self, position):
        return self._map[position]

    def print(self) -> None:
        for row in self._map:
            print(row)

    def _generate(self) -> list[str]:
        result_map = []
        for _ in range(self._map_length):
            cell_type = self._get_cell_type()
            result_map.append(cell_type * self._runners_count)

        return result_map

    def _get_cell_type(self) -> str:
        rand = random()

        cell_type = 'e'
        if 0.7 < rand < 0.9:
            cell_type = 'b'
        elif 0.9 < rand:
            cell_type = 'h'

        return cell_type


class Runner:
    def __init__(self, position: int):
        self._position = position
        self._speed_per_second = 0.99
        print(f'Hi, I am number {self._position} runner and my speed is {self._speed_per_second}')

    def run(self, runner_map: Map):
        meters_ran = 0
        while meters_ran < runner_map.length:  # пока не добежит до финиша
            runner_row = runner_map.get_row(int(meters_ran))  # получить строку по которой он бежит
            cell = runner_row[self._position]  # получить что там в конкретно его секторе
            if cell == 'e':  # если ячейка пуста
                sleep(0.01)  #
            elif cell == 'b':
                sleep(0.02)
            elif cell == 'h':
                sleep(0.04)
            meters_ran += self._speed_per_second

        global_print_lock.acquire()
        print(f'hey, its number {self._position} runner finished his run')
        global_print_lock.release()


class Game:
    def __init__(self, runners_map, runners):
        self._map = runners_map
        self._runners = runners

    def start(self):
        processes = [
            Thread(target=runner.run, args=(self._map, ))
            for runner in self._runners
        ]
        for process in processes:
            process.start()

        print('Game started')

        for process in processes:
            process.join()

        print('Game finished')


def main():
    print('Program with threads with locks')
    runners_count = 5  # количество бегунов
    lenght = 10  # длина трассы

    runners_map = Map(runners_count, lenght)
    runners_map.print()

    runners = [
        Runner(runner_number)
        for runner_number in range(runners_count)
    ]

    game = Game(runners_map, runners)
    game.start()


if __name__ == '__main__':
    main()
