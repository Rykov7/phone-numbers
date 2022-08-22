""" Module comparer.py - Compare tables. """
import os
import logging
import sys
from pathlib import Path
import csv
from colored import fg, attr
from fixer import Fixer
from config import LOG_MODE
from pie import make_plot

logging.basicConfig(level=LOG_MODE, format=f'{fg("yellow")}%(message)s{attr("reset")}')


class Comparer(Fixer):
    """ Comparer. """

    def __init__(self):
        super().__init__()
        self.dir_used = 'Used'
        self.dir_result = '[COMPARER]'
        self.used_tables = self.find_used()
        self.all_overlap = set()
        self.all_origin = set([i[0] for i in self.all_numbers])
        self.all_numbers = set([i[0] for i in self.all_numbers])

    def greeting(self):
        """ Program greeting. """
        print('COMPARER'.rjust(self.win_with))
        print('Сравнивает выбранную таблицу с таблицами в папке "Used"'.rjust(self.win_with))
        print()

    def find_used(self):
        """ Find CSVs in "Used" folder. """
        used_tables = []
        for folder_name, sub_folders, filenames in os.walk(Path(self.dir_used)):
            for file in Path(folder_name).glob('*.csv'):
                used_tables.append(file)
        if not used_tables:
            print('\nВ папке Used отсутствуют CSV!')
            sys.exit()
        return used_tables

    @Fixer.stopwatch
    def compare(self):
        """ Compare the table to the data-sets. """
        for used_table in self.used_tables:
            """ Проход по CSV-файлам в Used. """
            print(f"{used_table}")
            with open(used_table, 'r', newline='', encoding='utf-8') as csvfile:
                dubbed = {i[0] for i in csv.reader(csvfile)}

            dubbed &= self.all_numbers  # Detect current overlaps.
            self.all_origin -= dubbed   # Detect non-overlaps.
            self.all_overlap |= dubbed  # Detect all overlaps.

            curr_table_eq = len(dubbed) / (len(self.all_numbers) / 100)
            self.color_range(curr_table_eq)
            print(f'  └ СХОДСТВ: {len(dubbed):,} ({curr_table_eq:.0f}%)\n{attr("reset")}')

    def result(self):
        """ Print overall result. """
        table_eq = len(self.all_overlap) / (len(self.all_numbers) / 100)
        self.color_range(table_eq)
        print('[ РЕЗУЛЬТАТ СРАВНЕНИЯ ]'.center(self.win_with, '.'))
        print(f'\nОБЩЕЕ СХОДСТВО: {len(self.all_overlap):,}/{len(self.all_numbers):,} ({table_eq:.0f}%)\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))

    def save_everything(self):
        """ Save all CSVs. """
        os.makedirs(self.dir_result + os.sep + self.basename, exist_ok=True)
        self._save_rows(self.all_origin, self.dir_result + os.sep + self.basename + os.sep + self.basename + '[ORIGIN].csv')
        self._save_rows(self.all_overlap, self.dir_result + os.sep + self.basename + os.sep + self.basename + '[OVERLAP].csv')


if __name__ == '__main__':
    comparer = Comparer()
    comparer.compare()
    comparer.result()
    comparer.save_everything()

    make_plot(comparer.dir_result + os.sep + comparer.basename + os.sep + comparer.basename + '.png', comparer.filename,
              len(comparer.all_origin), len(comparer.all_overlap))
    comparer.russian_flag()
