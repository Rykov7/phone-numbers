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
        self.all_dubbed = []
        self.full_difference = -1111
        self.result_dir = 'RESULT'
        self.all_valid = self.all_numbers[:]

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
            dubbed = []
            print()
            print(f"[ {used_table} ]".center(self.win_with))

            with open(used_table, 'r', newline='') as csvfile:
                used_numbers = [i[0] for i in list(csv.reader(csvfile))]

            for used_number in used_numbers:
                if used_number in self.all_numbers:
                    dubbed.append(used_number)
                    print(f'{bg("red")}{used_number} есть в старой таблице!{attr("reset")}')
                    self.all_dubbed.append(used_number)
                    if used_number in self.all_valid:
                        self.all_valid.remove(used_number)
            print()
            print('[ ТЕКУЩЕЕ СРАВНЕНИЕ ]'.center(self.win_with, '.'))

            curr_table_eq = round((len(dubbed) / (len(self.all_numbers) / 100)), 2)

            if curr_table_eq < 5:
                print(bg("green"))
            elif curr_table_eq < 20:
                print(bg("yellow"))
            elif curr_table_eq < 50:
                print(bg("orange_red_1"))
            else:
                print(bg("red"))
            print(f'Пересечений с {used_table}: {len(dubbed)} ')
            print(f'СХОДСТВО: {curr_table_eq}%')
            print(attr("reset"))

    def overall(self):
        self.full_difference = round((len(self.valid_numbers) / (len(self.all_numbers)/100)), 2)

        if self.full_difference < 60:
            print(bg("red"))
        elif self.full_difference < 70:
            print(bg("orange_red_1"))
        elif self.full_difference < 90:
            print(bg("yellow"))
        else:
            print(bg("green"))
        print('[ РЕЗУЛЬТАТ ]'.center(self.win_with, '.'))
        print(f'\nКАЧЕСТВО: {self.full_difference}% ({len(self.all_dubbed)}/{len(self.all_numbers)})')
        print(attr("reset"))

    def save_everything(self):
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.all_dubbed, self.result_dir + os.sep + self.filename[:-4] + '_[ALL_DUBBED].csv')
        self._save_numbers(self.all_valid, self.result_dir + os.sep + self.filename[:-4] + '_[ALL_VALID].csv')


if __name__ == '__main__':
    comparer = Comparer()
    comparer.compare()
    comparer.overall()
    comparer.save_everything()
