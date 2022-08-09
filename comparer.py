""" Модуль comparer.py - Сравнивает новую таблицу номеров со старыми. """
import os
import logging
import sys
from pathlib import Path
import csv
from datetime import datetime as dt
from colored import fg, attr
from fixer import Fixer
from config import LOG_MODE
from pie import make_plot

logging.basicConfig(level=LOG_MODE, format=f'{fg("yellow")}%(message)s{attr("reset")}')


class Comparer(Fixer):
    """ Сравниватель. """
    def __init__(self):
        super().__init__()
        self.dir_used = 'Used'  # Папка со старыми CSV.
        self.dir_result = '[COMPARER]'
        self.used_tables = self.find_used()
        self.all_overlap = set()
        self.all_origin = set(self.all_numbers)
        self.all_numbers = set(self.all_numbers)

    def greeting(self):
        """ Приветствие программы. """
        print('СРАВНИВАТЕЛЬ'.rjust(self.win_with))
        print('Сравнивает выбранную таблицу с таблицами в папке "Used"'.rjust(self.win_with))
        print()

    def find_used(self):
        """ Ищет CSV в "Used" для сравнения с проверяемым CSV. """
        used_tables = []
        for folder_name, sub_folders, filenames in os.walk(Path(self.dir_used)):
            for file in Path(folder_name).glob('*.csv'):
                used_tables.append(file)
        if not used_tables:
            print('\nВ папке Used отсутствуют CSV!')
            sys.exit()
        return used_tables

    def compare(self):
        """ Сравнивает таблицу с базой. """
        for used_table in self.used_tables:
            """ Проход по CSV-файлам в Used. """
            print(f"{used_table}")
            with open(used_table, 'r', newline='', encoding='utf-8') as csvfile:
                dubbed = set([i[0] for i in csv.reader(csvfile)])

            dubbed &= self.all_numbers    # Расчёт пересечения текущего файла со всеми.
            self.all_origin -= dubbed     # Расчёт не пересёкшихся номеров.
            self.all_overlap |= dubbed    # Расчёт всех пересёкшимся.

            curr_table_eq = round((len(dubbed) / (len(self.all_numbers) / 100)), 2)
            self.color_range(curr_table_eq)
            print(f'  └ СХОДСТВО: {curr_table_eq}% ({len(dubbed)}/{len(self.all_numbers)})\n{attr("reset")}')

    def result(self):
        """ Печатает общий результат. """
        table_eq = round(len(self.all_overlap) / (len(self.all_numbers)/100))
        self.color_range(table_eq)
        print('[ РЕЗУЛЬТАТ СРАВНЕНИЯ ]'.center(self.win_with, '.'))
        print(f'\nОБЩЕЕ СХОДСТВО: {table_eq}% ({len(self.all_overlap)}/{len(self.all_numbers)})\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))

    def save_everything(self):
        """ Сохраняет все CSV-файлы. """
        os.makedirs(self.dir_result, exist_ok=True)
        self._save_numbers(self.all_origin, self.dir_result + os.sep + self.filename[:-4] + '[ORIGIN].csv')
        self._save_numbers(self.all_overlap, self.dir_result + os.sep + self.filename[:-4] + '[OVERLAP].csv')


if __name__ == '__main__':
    comparer = Comparer()
    start = dt.now()
    comparer.compare()
    end = dt.now() - start
    print(f"Время обработки: {end.seconds} сек.")
    comparer.result()
    comparer.save_everything()

    # Сохраняет изображение с графиком.
    make_plot(comparer.dir_result + os.sep + comparer.filename[:-4] + '.png', comparer.filename,
              len(comparer.all_origin), len(comparer.all_overlap))
    comparer.russian_flag()
