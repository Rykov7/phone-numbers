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
        self.all_dubbed_counter = 0
        self.full_difference = -1111
        self.result_dir = 'ОТЧЁТ'

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
        self.valid_numbers = self.all_numbers
        for used_table in self.used_tables:
            print()
            print(f"[ {used_table} ]".center(self.win_with))
            dubbed = []
            with open(used_table, 'r', newline='') as csvfile:
                used_numbers = list(csv.reader(csvfile))

            for used_number in used_numbers:
                if used_number in self.all_numbers:
                    print(f'{bg("red")}{used_number[0]} уже есть в старой таблице!{attr("reset")}')
                    curr_ind = self.all_numbers.index(used_number)
                    dubbed.append(used_number)
                    self.all_dubbed.append(used_number[0])
                    self.valid_numbers.pop(curr_ind)
                    self.all_dubbed_counter += 1

            dubbed_count = len(dubbed)
            print()
            print('[ ИТОГ ]'.center(self.win_with, '.'))

            current_table_equality = round(100 - (len(self.all_numbers) - dubbed_count) / (len(self.all_numbers) / 100),
                                           2)

            if current_table_equality < 10:
                print(bg("green"))
            elif current_table_equality < 30:
                print(bg("yellow"))
            elif current_table_equality < 50:
                print(bg("orange_red_1"))
            else:
                print(bg("red"))
            print(f'Пересечений с {used_table}: {dubbed_count} ')
            print(f'СОВПАДЕНИЕ С ТЕКУЩЕЙ ТАБЛИЦЕЙ: {current_table_equality}%')
            print(attr("reset"))

    def overall(self):
        self.full_difference = round((len(self.all_numbers)-self.all_dubbed_counter)/(len(self.all_numbers)/100), 2)
        if self.full_difference < 60:
            print(bg("red"))
        elif self.full_difference < 70:
            print(bg("orange_red_1"))
        elif self.full_difference < 90:
            print(bg("yellow"))
        else:
            print(bg("green"))
        print(f'\nОБЩАЯ УНИКАЛЬНОСТЬ: {self.full_difference}%')
        print(f'Сходство со старыми: {self.all_dubbed_counter}/{len(self.all_numbers)} ')
        print(attr("reset"))

    def save_everything(self):
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.all_dubbed, self.result_dir + os.sep + self.filename[:-4] + '_[ALL_DUBBED].csv')
        self._save_numbers(self.valid_numbers, self.result_dir + os.sep + self.filename[:-4] + '_[ALL_VALID].csv')

if __name__ == '__main__':
    comparer = Comparer()
    comparer.compare()
    comparer.overall()
    comparer.save_everything()
