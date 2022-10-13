#!python3

""" Module comparer.py - Compare tables. """
import os
import logging
import sys
from pathlib import Path
import csv
from colored import fg, attr
from fixer import Fixer
from config import LOG_MODE, ENCODING_READ, DELIMITER
from pie import make_plot

logging.basicConfig(level=LOG_MODE, format=f'{fg("yellow")}%(message)s{attr("reset")}')


class Comparer(Fixer):
    """ Comparer. Main class. """

    def __init__(self):
        super().__init__()
        self.dir_used = 'Used'
        self.dir_result = '[COMPARER]'
        self.used_tables = self.find_used()
        self.overlaps = set()
        self.unique = {i[0] for i in self.all_columns}
        self.all_numbers = self.unique.copy()

    def greeting(self):
        """ Program greeting. """
        print('COMPARER'.rjust(self.win_with))
        print('Выводит статистику по сходству номеров'.rjust(self.win_with))
        self.show_config()
        print()

    def find_used(self):
        """ Find CSVs in "Used" folder. """
        used_tables = []
        for folder_name, sub_folders, filenames in os.walk(Path(self.dir_used)):
            for file in Path(folder_name).glob('*.csv'):
                used_tables.append(file)
        if not used_tables:
            print('\nВ папке Used отсутствуют CSV-файлы!')
            sys.exit()
        return used_tables

    @staticmethod
    def test_number(number: str):
        try:
            assert len(number) == 11 and number.startswith('79')
        except AssertionError:
            print(fg('red_3a') + f'Ошибка результата! Формат проверяемого номера ({number}) не соответствует формату '
                                 '79XXXXXXXXX. Вероятно выбран невалидный файл!' + attr('reset'))
            sys.exit(1)

    @Fixer.stopwatch
    def compare(self):
        self.test_number(list(self.all_numbers)[-1])

        """ Compare the table to the data-sets. """
        for used_table in self.used_tables:
            """ Проход по CSV-файлам в Used. """
            print(f"{used_table}")
            with open(used_table, 'r', newline='', encoding=ENCODING_READ) as csvfile:
                dubbed = {i[0] for i in csv.reader(csvfile, dialect='excel', delimiter=DELIMITER)}

            dubbed &= self.all_numbers  # Detect current overlaps.
            self.unique -= dubbed  # Detect non-overlaps.
            self.overlaps |= dubbed  # Detect all overlaps.

            curr_table_eq = len(dubbed) / (len(self.all_columns) / 100)
            self.color_range(curr_table_eq)
            print(f'  └ СХОДСТВ: {len(dubbed):,} ({curr_table_eq:.0f}%)\n{attr("reset")}')

        self.unique = [i for i in self.all_columns if i[0] in self.unique]
        self.overlaps = [[i] for i in self.overlaps]

    def result(self):
        """ Print overall result. """
        table_eq = len(self.overlaps) / (len(self.all_columns) / 100)
        self.color_range(table_eq)
        print('[ РЕЗУЛЬТАТ СРАВНЕНИЯ ]'.center(self.win_with, '.'))
        print(f'\nОБЩЕЕ СХОДСТВО: {len(self.overlaps):,}/{len(self.all_numbers):,} ({table_eq:.0f}%)\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))

    def save_everything(self):
        """ Save all CSVs. """
        os.makedirs(self.dir_result + os.sep + self.basename, exist_ok=True)
        self._save_rows(self.unique,
                        self.dir_result + os.sep + self.basename + os.sep + self.basename + '[UNIQUE].csv')
        self._save_rows(self.overlaps,
                        self.dir_result + os.sep + self.basename + os.sep + self.basename + '[OVERLAP].csv')


if __name__ == '__main__':
    q = ''
    while q.lower() not in ('q', 'й'):
        comparer = Comparer()
        comparer.compare()
        comparer.result()
        comparer.save_everything()

        make_plot(comparer.dir_result + os.sep + comparer.basename + os.sep + comparer.basename + '.png',
                  comparer.filename, len(comparer.unique), len(comparer.overlaps))
        comparer.print_flag()
        q = input('ENTER чтобы выбрать другую таблицу (Q - выход): ')
        os.system('cls') and os.system('clear')
