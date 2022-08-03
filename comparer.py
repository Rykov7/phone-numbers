""" compare.py - Сравнивает новую таблицу номеров со старыми. """

import os
import logging
from pathlib import Path
import csv
from colored import bg, fg, attr
from fixer import Analyzer
from config import LOG_MODE

logging.basicConfig(level=LOG_MODE, format='%(levelname)s - %(message)s')


class Comparer(Analyzer):
    def __init__(self):
        super().__init__()
        self.used_location = 'used'
        self.used_tables = self.find_used()
        self.all_dubbed = []
        self.full_difference = -1111
        self.result_dir = '[COMPARER_RESULT]'
        self.all_valid = self.all_numbers[:]
        self.table_eq = 0

    def greeting(self):
        print('СРАВНИВАТЕЛЬ'.rjust(self.win_with))
        print('Сравнивает новую таблицу со старыми в папке "used"'.rjust(self.win_with))
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
            print(f"{used_table}")
            with open(used_table, 'r', newline='', encoding='utf-8') as csvfile:
                used_numbers = [i[0] for i in list(csv.reader(csvfile))]

            for used_number in used_numbers:
                if used_number in self.all_numbers:
                    dubbed.append(used_number)
                    logging.info(f'{bg("red")}{used_number} есть в старой таблице!{attr("reset")}')
                    self.all_dubbed.append(used_number)
                    if used_number in self.all_valid:
                        self.all_valid.remove(used_number)

            curr_table_eq = round((len(dubbed) / (len(self.all_numbers) / 100)), 2)
            color_range(curr_table_eq)

            print(f'  └ СХОДСТВО: {curr_table_eq}% ({len(dubbed)}/{len(self.all_numbers)})\n{attr("reset")}')

    def overall(self):
        self.table_eq = round((len(self.all_dubbed) / (len(self.all_numbers)/100)), 2)
        color_range(self.table_eq)
        print('[ РЕЗУЛЬТАТ ]'.center(self.win_with, '.'))
        print(f'ОБЩЕЕ СХОДСТВО: {self.table_eq}% ({len(self.all_dubbed)}/{len(self.all_numbers)}){attr("reset")}')

    def save_everything(self):
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.all_dubbed, self.result_dir + os.sep + self.filename[:-4] + '[ALL_DUBBED].csv')
        self._save_numbers(self.all_valid, self.result_dir + os.sep + self.filename[:-4] + '[ALL_VALID].csv')

    def russian_flag(self):
        print()
        print(bg("white") + fg("white") + 'R' * self.win_with + attr("reset"))
        print(bg("blue") + fg("blue") + 'U' * self.win_with + attr("reset"))
        print(bg("red") + fg("red") + 'S' * self.win_with + attr("reset"))


def color_range(numb):
    if numb < 5:
        print(fg("green"), end='')
    elif numb < 20:
        print(fg("yellow"), end='')
    elif numb < 50:
        print(fg("orange_red_1"), end='')
    else:
        print(fg("red"), end='')


def russian_flag():
    print()
    print(bg("white") + ' '*100 + attr("reset"))
    print(bg("blue") + ' '*100 + attr("reset"))
    print(bg("red") + ' '*100 + attr("reset"))


if __name__ == '__main__':
    comparer = Comparer()
    comparer.compare()
    comparer.overall()
    comparer.save_everything()

    comparer.russian_flag()
