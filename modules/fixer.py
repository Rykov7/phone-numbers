""" Module fixer.py - fix phone numbers to 79XXXXXXXXX. """
import csv
import os
import sys
import re
import logging
from datetime import datetime as dt
from pathlib import Path
from colored import bg, fg, attr

from config import LOG_MODE, WIN_WIDTH, ENCODING_READ, ENCODING_WRITE
from pie import make_plot

logging.basicConfig(level=LOG_MODE, format=f'{fg("yellow")}%(message)s{attr("reset")}')


class Fixer:
    """ Fixer. """

    def __init__(self):
        self.win_with = WIN_WIDTH
        self.greeting()
        self.junk, self.dubbed, = [], []
        self.valid = set()
        self.filename = self.find_new()
        self.all_numbers = self.open_csv()
        self.result_dir = '[FIXER]'

    def greeting(self):
        """ Program greeting. """
        print('FIXER'.rjust(self.win_with))
        print('Исправляет телефонные номера до формата 79XXXXXXXXX'.rjust(self.win_with))
        print()

    @staticmethod
    def _which_file(question: str, allow_range: int) -> int:
        """ Validate file number. """
        while True:
            answer = input(question)
            if answer.isdigit() and int(answer) in range(1, allow_range + 1):
                return int(answer)

    def find_new(self) -> str:
        """ Find all CSVs in the work directory. Returns filename string. """
        all_files = list(Path().glob('*.csv'))
        if all_files:
            print("CSV в текущей папке:")
            for file in all_files:
                file_option_string = f'  {all_files.index(file) + 1}. {str(file)}{fg("#444")}'
                file_size_string = f'{attr("reset")}{int(os.path.getsize(file) / 1024):,} KB'
                # Adding 15 of colored special characters.
                print(f'{file_option_string}'.ljust(self.win_with - len(file_size_string) + 15, '.'), end='')
                print(f'{file_size_string}')
            print()
            if len(all_files) == 1:
                choose = self._which_file(f'Выберите файл для обработки (1): ', 1)
            else:
                choose = self._which_file(f'Выберите файл для обработки (1-{len(all_files)}): ', len(all_files))
            print()
            return str(all_files[choose - 1])
        else:
            print(f'Для начала работы добавьте CSV в текущую папку:\n{Path.cwd()}\n')
            sys.exit()

    def open_csv(self) -> list[str]:
        """ Convert CSV into list. """
        try:
            with open(self.filename, 'r', newline='', encoding=ENCODING_READ) as csvfile:
                return [i[0] for i in csv.reader(csvfile, dialect='excel', delimiter=';') if i]
        except UnicodeDecodeError:
            print(f'{bg("red_3a")}ОШИБКА! Неверная кодировка файла!{attr("reset")}.')
            sys.exit()

    @staticmethod
    def correct_number(number: str) -> str:
        """ Fix phone number to 79XXXXXXXXX. """
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

    @staticmethod
    def stopwatch(func):
        def wrapper(*args):
            start = dt.now()  # Стартовое время для определения скорости работы.
            func(*args)
            end = dt.now() - start
            print(f"{fg('#444')}Время обработки: {end.seconds} сек.{attr('reset')}")

        return wrapper

    @stopwatch
    def fix(self):
        """ Analyse and fix phone numbers. """
        for number in self.all_numbers:
            number = self.correct_number(number)
            if len(number) != 11 or not number.startswith('79') or not number.isdigit() or \
                    re.search(r'(\d)\1{6}', number):
                logging.warning(f"Нашёл некорректную запись {number}")
                self.junk.append(number)
                continue
            if number in self.valid:
                logging.warning(f"Нашёл дубликат {number}")
                self.dubbed.append(number)
            else:
                self.valid.add(number)

    def result(self):
        """ Print stats REPORT. """
        all_numbers_count = len(self.all_numbers)
        junk_count = len(self.junk)
        valid_count = len(self.valid)
        self.color_range(round(100 - valid_count / (all_numbers_count / 100)))  # Set result block color.
        print('[ РЕЗУЛЬТАТ ИСПРАВЛЕНИЙ ]'.center(self.win_with, '.'))
        print(f'\nПЛОХИЕ: {junk_count + len(self.dubbed):,}')
        print(f'  ├ повторы: {len(self.dubbed):,}')
        print(f'  └ мусор: {junk_count:,}')
        print(f'\nНОМЕРА: {valid_count / all_numbers_count:.0%} ({valid_count:,}/{all_numbers_count:,})\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))                                                    # Reset result block color.

    @staticmethod
    def _save_numbers(numbs, filename):
        """ Save number list to CSV file. """
        if numbs:  # Save CSV if not empty.
            with open(filename, 'w', newline='', encoding=ENCODING_WRITE) as file:
                writer = csv.writer(file, dialect='excel', delimiter=';')
                for numb in numbs:
                    writer.writerow([numb])
            print(f'{bg("dodger_blue_3")}[CSV] {len(numbs)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        """ Save all CSVs. """
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(sorted(self.valid), self.result_dir + os.sep + self.filename[:-4] + '[valid].csv')
        self._save_numbers(set(self.dubbed), self.result_dir + os.sep + self.filename[:-4] + '[dubs].csv')
        self._save_numbers(self.junk, self.result_dir + os.sep + self.filename[:-4] + '[junk].csv')

    @staticmethod
    def color_range(numb):
        """ Calculate text color based on stats. """
        if numb < 4:
            print(fg("#52a7563"), end='')  # green
        elif numb < 30:
            print(fg("yellow"), end='')
        elif numb < 60:
            print(fg("orange_red_1"), end='')
        else:
            print(fg("#e51c24"), end='')  # red

    def russian_flag(self):
        """ Print flag. """
        print()
        print(bg("cornsilk_1") + fg("cornsilk_1") + 'R' * self.win_with + attr("reset"))
        print(bg("dodger_blue_3") + fg("dodger_blue_3") + 'U' * self.win_with + attr("reset"))
        print(bg("red_3a") + fg("red_3a") + 'S' * self.win_with + attr("reset"))


if __name__ == '__main__':
    fixer = Fixer()
    fixer.fix()
    fixer.result()
    fixer.save_everything()

    make_plot(fixer.result_dir + os.sep + fixer.filename[:-4] + '.png', fixer.filename,
              len(fixer.valid), len(fixer.dubbed), len(fixer.junk))
    fixer.russian_flag()
