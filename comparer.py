""" Модуль comparer.py - Сравнивает новую таблицу номеров со старыми. """
import os
import logging
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
        self.used_location = 'Used'  # Папка со старыми CSV.
        self.used_tables = self.find_used()
        self.all_overlap = []
        self.all_origin = set()
        self.result_dir = '[COMPARER]'
        self.all_numbers = set(self.all_numbers)  # Перевод в хэш для скорости.

    def greeting(self):
        """ Приветствие программы. """
        print('СРАВНИВАТЕЛЬ'.rjust(self.win_with))
        print('Сравнивает выбранную таблицу с таблицами в папке "Used"'.rjust(self.win_with))
        print()

    def find_used(self):
        """ Ищет CSV в "Used" для сравнения с проверяемым CSV. """
        used_tables = []
        for folder_name, sub_folders, filenames in os.walk(Path(self.used_location)):
            for file in Path(folder_name).glob('*.csv'):
                used_tables.append(file)
        return used_tables

    def compare(self):
        """ Сравнивает таблицу с базой. """
        for used_table in self.used_tables:
            """ Проход по CSV-файлам в Used. """
            print(f"{used_table}")
            with open(used_table, 'r', newline='', encoding='utf-8') as csvfile:
                used_numbers = set([i[0] for i in csv.reader(csvfile)])

            dubbed = used_numbers & self.all_numbers     # Пересечения
            self.all_origin = self.all_numbers - dubbed  # Оригиналы (без пересечений)
            self.all_overlap.extend(dubbed)              # Добавляем текущие дубли к общим.

            curr_table_eq = round((len(dubbed) / (len(self.all_numbers) / 100)), 2)
            self.color_range(curr_table_eq)
            print(f'  └ СХОДСТВО: {curr_table_eq}% ({len(dubbed)}/{len(self.all_numbers)})\n{attr("reset")}')

    def overall(self):
        """ Печатает общий результат. """
        table_eq = int((len(self.all_overlap) / (len(self.all_numbers)/100)))
        self.color_range(table_eq)
        print('[ РЕЗУЛЬТАТ СРАВНЕНИЯ ]'.center(self.win_with, '.'))
        print(f'\nОБЩЕЕ СХОДСТВО: {table_eq}% ({len(self.all_overlap)}/{len(self.all_numbers)})\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))

    def save_everything(self):
        """ Сохраняет все CSV-файлы. """
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.all_origin, self.result_dir + os.sep + self.filename[:-4] + '[ORIGIN].csv')
        self._save_numbers(self.all_overlap, self.result_dir + os.sep + self.filename[:-4] + '[OVERLAP].csv')


if __name__ == '__main__':
    comparer = Comparer()
    start = dt.now()
    comparer.compare()
    end = dt.now() - start
    print(f"Время обработки: {end.seconds} сек.")
    comparer.overall()
    comparer.save_everything()

    # Сохраняет изображение с графиком.
    make_plot(comparer.result_dir + os.sep + comparer.filename[:-4] + '.png', comparer.filename,
              len(comparer.all_origin), len(comparer.all_overlap))
    comparer.russian_flag()
