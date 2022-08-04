""" comparer.py - Сравнивает новую таблицу номеров со старыми. """
import os
import logging
from pathlib import Path
import csv
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
        self.all_dubbed = []
        self.table_eq = 0
        self.full_difference = 0
        self.all_valid = self.all_numbers[:]
        self.result_dir = '[COMPARER]'

    def greeting(self):
        """ Приветствие программы. """
        print('СРАВНИВАТЕЛЬ'.rjust(self.win_with))
        print('Сравнивает выбранную таблицу с таблицами в папке "Used"'.rjust(self.win_with))
        print()

    def find_used(self):
        """ Ищет CSV в "Used" для сравнения с проверяемым CSV. """
        used_tables = []
        for folder_name, subfolders, filenames in os.walk(Path(self.used_location)):
            for file in Path(folder_name).glob('*.csv'):
                used_tables.append(file)
        return used_tables

    def compare(self):
        """ Сравнивает таблицу с базой. """
        for used_table in self.used_tables:
            dubbed = []
            print(f"{used_table}")
            with open(used_table, 'r', newline='', encoding='utf-8') as csvfile:
                used_numbers = [i[0] for i in list(csv.reader(csvfile))]

            for new_number in self.all_numbers:
                if new_number in used_numbers:                      # Если новый номер в базе.
                    dubbed.append(new_number)                       # Помечаем как текущий дубль.
                    logging.warning(f'Нашёл дубль {new_number}!')
                    self.all_dubbed.append(new_number)              # Помечаем как общий дубль.
                    if new_number in self.all_valid:
                        self.all_valid.remove(new_number)           # Удаляем из списка валидных.

            curr_table_eq = round((len(dubbed) / (len(self.all_numbers) / 100)), 2)
            self.color_range(curr_table_eq)
            print(f'  └ СХОДСТВО: {curr_table_eq}% ({len(dubbed)}/{len(self.all_numbers)})\n{attr("reset")}')

    def overall(self):
        """ Печатает общий результат. """
        self.table_eq = int((len(self.all_dubbed) / (len(self.all_numbers)/100)))
        self.color_range(self.table_eq)
        print('[ РЕЗУЛЬТАТ СРАВНЕНИЯ ]'.center(self.win_with, '.'))
        print(f'\nОБЩЕЕ СХОДСТВО: {self.table_eq}% ({len(self.all_dubbed)}/{len(self.all_numbers)})\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))

    def save_everything(self):
        """ Сохраняет все CSV-файлы. """
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.all_valid, self.result_dir + os.sep + self.filename[:-4] + '[VALID].csv')
        self._save_numbers(self.all_dubbed, self.result_dir + os.sep + self.filename[:-4] + '[DUBS].csv')


if __name__ == '__main__':
    comparer = Comparer()
    comparer.compare()
    comparer.overall()
    comparer.save_everything()

    # Сохраняет изображение с графиком.
    make_plot(comparer.result_dir + os.sep + comparer.filename[:-4] + '.png', comparer.filename,
              len(comparer.all_valid), len(comparer.all_dubbed))
    comparer.russian_flag()