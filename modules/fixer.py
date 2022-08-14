""" Module fixer.py - fixes phone numbers to 79XXXXXXXXX format. """
import csv
import os
import sys
import re
import logging
from datetime import datetime as dt
from pathlib import Path
from colored import bg, fg, attr
from config import LOG_MODE, WIN_WIDTH
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
        print('ИСПРАВЛЯТОР'.rjust(self.win_with))
        print('Приводит телефонные номера к формату 79XXXXXXXXX'.rjust(self.win_with))
        print()

    @staticmethod
    def _which_file(question: str, allow_range: int) -> int:
        """ Validates file number. """
        while True:
            answer = input(question)
            if answer.isdigit() and int(answer) in range(1, allow_range + 1):
                return int(answer)

    def find_new(self) -> str:
        """ Finds all CSVs in the work directory. Returns filename string. """
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
            return str(all_files[choose - 1])
        else:
            print(f'Для начала работы добавьте CSV в текущую папку:\n{Path.cwd()}\n')
            sys.exit()

    def open_csv(self) -> list[str]:
        """ Reads CSV into list. """
        with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
            return [i[0] for i in csv.reader(csvfile) if i]

    @staticmethod
    def correct_number(number: str) -> str:
        """ Fixes a phone number to 79XXXXXXXXX format. """
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

    def fix(self):
        """ Analyses and fixes phone numbers. """
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
        """ Prints stats REPORT. """
        all_numbers_count = len(self.all_numbers)
        junk_count = len(self.junk)  # Junk strings
        valid_count = len(self.valid)  # Valid numbers
        print()
        self.color_range(round(100 - valid_count / (all_numbers_count / 100)))
        print('[ РЕЗУЛЬТАТ ИСПРАВЛЕНИЙ ]'.center(self.win_with, '.'))
        print(f'\nПЛОХИЕ: {junk_count + len(self.dubbed):,}')
        print(f'  ├ повторы: {len(self.dubbed):,}')
        print(f'  └ мусор: {junk_count:,}')
        print(f'\nНОМЕРА: {valid_count / all_numbers_count:.0%} ({valid_count:,}/{all_numbers_count:,})\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))

    @staticmethod
    def _save_numbers(numbs, filename):
        """ Saves number list to CSV file. """
        if numbs:  # Saves csv if it isn't empty.
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for numb in numbs:
                    writer.writerow([numb])
            print(f'{bg("dodger_blue_3")}[CSV] {len(numbs)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        """ Saves all CSVs. """
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(sorted(self.valid), self.result_dir + os.sep + self.filename[:-4] + '[valid].csv')
        self._save_numbers(set(self.dubbed), self.result_dir + os.sep + self.filename[:-4] + '[dubs].csv')
        self._save_numbers(self.junk, self.result_dir + os.sep + self.filename[:-4] + '[junk].csv')

    @staticmethod
    def color_range(numb):
        """ Calculates text color based on stats. """
        if numb < 4:
            print(fg("#52a7563"), end='')  # green
        elif numb < 30:
            print(fg("yellow"), end='')
        elif numb < 60:
            print(fg("orange_red_1"), end='')
        else:
            print(fg("#e51c24"), end='')  # red

    def russian_flag(self):
        """ Prints Russia's flag. """
        print()
        print(bg("cornsilk_1") + fg("cornsilk_1") + 'R' * self.win_with + attr("reset"))
        print(bg("dodger_blue_3") + fg("dodger_blue_3") + 'U' * self.win_with + attr("reset"))
        print(bg("red_3a") + fg("red_3a") + 'S' * self.win_with + attr("reset"))


if __name__ == '__main__':
    fixer = Fixer()
    start = dt.now()  # Стартовое время для определения скорости работы.
    fixer.fix()
    end = dt.now() - start
    print(f"Время обработки: {end.seconds} сек.")
    fixer.result()
    fixer.save_everything()  # Сохраняет изображение с графиком.

    make_plot(fixer.result_dir + os.sep + fixer.filename[:-4] + '.png', fixer.filename,
              len(fixer.valid), len(fixer.dubbed), len(fixer.junk))
    fixer.russian_flag()
