""" comparison.py - Сравнивает новую таблицу номеров со старыми. """

import os
from pathlib import Path
import csv
from colored import bg, attr
from fix_numbers import Analyzer


class Comparer(Analyzer):
    def __init__(self):
        super().__init__()
        self.used_location = 'used'
        self.used_tables = self.find_used()
        self.all_dubbed_counter = 0

    def greeting(self):
        print('comparison.py'.rjust(100))
        print('Сравнивает новую таблицу со старыми'.rjust(self.win_with))
        print()

    def find_used(self):
        used_tables = []
        for folder_name, subfolders, filenames in os.walk(Path(self.used_location)):
            for file in Path(folder_name).glob('*.csv'):
                used_tables.append(file)
        return used_tables

    def compare(self):
        for used_table in self.used_tables:
            print(f"\nТАБЛИЦА: {used_table}")
            dubbed = []
            with open(used_table, 'r', newline='') as csvfile:
                used_numbers = list(csv.reader(csvfile))

            for used_number in used_numbers:
                if used_number in self.all_numbers:
                    print(f'{bg("red")}{used_number[0]} уже есть в старой таблице!{attr("reset")}')
                    dubbed.append(used_number)
                    self.all_dubbed_counter += 1

            dubbed_count = len(dubbed)

            print()
            print('[ ОТЧЁТ ]'.center(100, '-'))
            print(f'Пересечений с {used_table}: {dubbed_count} ')
            print(f'СОВПАДЕНИЕ С ТЕКУЩЕЙ ТАБЛИЦЕЙ: '
                  f'{round(100 - (len(self.all_numbers)-dubbed_count)/(len(self.all_numbers)/100), 2)}%')
            print()

    def overall(self):
        print(f'Пересечений со всеми: {self.all_dubbed_counter} ')
        print(f'ОБЩАЯ УНИКАЛЬНОСТЬ: {round((len(self.all_numbers)-self.all_dubbed_counter)/(len(self.all_numbers)/100), 2)}%')


if __name__ == '__main__':
    comparer = Comparer()
    comparer.compare()
    comparer.overall()
