""" Module fixer_excel.py - fix phone numbers to 79XXXXXXXXX in 6th column, keep all columns. """
import csv
import os
import sys
import re
import logging

from colored import bg, fg, attr
from config import LOG_MODE, ENCODING_READ, ENCODING_WRITE, COLUMN, CHOP_HEADER
from pie import make_plot
from fixer import Fixer

logging.basicConfig(level=LOG_MODE, format=f'{fg("yellow")}%(message)s{attr("reset")}')


class MulticolumnFixer(Fixer):
    """ MultiColumnFixer. """

    def __init__(self):
        super().__init__()
        self.valid = []
        self.column = COLUMN - 1
        self.chop_head = CHOP_HEADER

    def greeting(self):
        """ Program greeting. """
        print('FIXER EXCEL С СОХРАНЕНИЕМ КОЛОНОК'.rjust(self.win_with))
        print('Исправляет телефонные номера в 6 столбце.'.rjust(self.win_with))
        print()

    def open_csv(self) -> list[list]:
        """ Reads CSV into list. """
        try:
            with open(self.filename, 'r', newline='', encoding=ENCODING_READ) as csvfile:
                return [i for i in csv.reader(csvfile, dialect='excel', delimiter=';') if i][CHOP_HEADER:]
        except UnicodeDecodeError:
            print(f'{bg("red_3a")}ОШИБКА! Выбрана некорректная кодировка файла! '
                  f'Нужна {ENCODING_READ}{attr("reset")}.')
            sys.exit()

    @staticmethod
    def correct_number(number: str) -> str:
        """ Fixes a phone number to 79XXXXXXXXX format. """
        number = number.split(',')[-1]
        if not number.isdigit():
            logging.info(f'{number} удалил лишние символы. ')
            for char in number:
                if not char.isdigit():
                    number = number.replace(char, '')  # Clear non-digital chars.
        if number.startswith('89') and len(number) == 11:
            logging.info(f'{number} исправил 8 на 7.')
            return '7' + number[1:]
        elif number.startswith('9') and len(number) == 10:
            logging.info(f'{number} добавил 7 перед номером.')
            return f'7' + number
        return number

    @Fixer.stopwatch
    def fix(self):
        """ Analyses and fixes phone numbers. """
        if len(self.all_numbers[-1]) < self.column:
            print('ОШИБКА! Номер колонки в настройках больше количества колонок! Выхожу.')
            sys.exit()
        for row in self.all_numbers:
            number = row[self.column]
            number = self.correct_number(number)
            row = [number] + row[:self.column] + row[self.column+1:]
            if len(number) != 11 or not number.startswith('79') or not number.isdigit() or \
                    re.search(r'(\d)\1{6}', number):
                logging.warning(f"Нашёл некорректную запись {number}")
                self.junk.append(row)
                continue

            if number in [i[0] for i in self.valid]:
                logging.warning(f"Нашёл дубликат {number}")
                self.dubbed.append(row)
            else:
                self.valid.append(row)

    @staticmethod
    def _save_rows(rows, filename):
        """ Saves number list to CSV file. """
        if rows:  # Save CSVs only with data.
            with open(filename, 'w', newline='', encoding=ENCODING_WRITE) as file:
                writer = csv.writer(file, dialect='excel', delimiter=';')
                for row in rows:
                    writer.writerow(row)
            print(f'{bg("dodger_blue_3")}[CSV] {len(rows)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        """ Saves all CSVs. """
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_rows(self.valid, self.result_dir + os.sep + self.filename[:-4] + '[valid].csv')
        self._save_rows(self.dubbed, self.result_dir + os.sep + self.filename[:-4] + '[dubs].csv')
        self._save_rows(self.junk, self.result_dir + os.sep + self.filename[:-4] + '[junk].csv')


if __name__ == '__main__':
    fixer = MulticolumnFixer()
    fixer.fix()
    fixer.result()
    fixer.save_everything()

    make_plot(fixer.result_dir + os.sep + fixer.filename[:-4] + '.png', fixer.filename,
              len(fixer.valid), len(fixer.dubbed), len(fixer.junk))
    fixer.russian_flag()
