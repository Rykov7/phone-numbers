#!python3

""" Fix phone numbers into 79XXXXXXXXX format. """
import csv
import os
import sys
import re
import logging
import platform
import subprocess
from pathlib import Path
from colored import bg, fg, attr

from stopwatch import stopwatch
from config import LOG_LEV, WIN_WIDTH, ENCODINGS_READ, ENCODING_WRITE, COLUMN, DELIMITER
from pie import make_plot

logging.basicConfig(level=LOG_LEV, format=f'{fg("yellow")}%(message)s{attr("reset")}')


class Fixer:
    """ Fixer. Main class. """

    def __init__(self):
        self.column = COLUMN - 1
        self.win_with = WIN_WIDTH
        self.greeting()
        self.junk, self.dubbed, = [], []
        self.valid = {}
        self.filename = self.find_new()
        self.basename = self.filename[:-4]
        self.all_columns = self.open_csv()
        self.dir_result = '[FIXER]'

    def greeting(self):
        """ Greet. """
        print('FIXER'.rjust(self.win_with))
        print(f'Нормализует телефонные номера в колонке: {COLUMN}'.rjust(self.win_with))
        self.show_config()

    def show_config(self):
        print(f'Чтение: автоопределение, запись {ENCODING_WRITE}'.rjust(self.win_with))
        print()

    def which_file(question: str, allow_range: int) -> int:
        """ Validate file number. """
        while True:
            answer = input(question)
            if answer.isdigit() and int(answer) in range(1, allow_range + 1):
                os.system('cls') and os.system('clear')  # clear screen Win and Unix
                return int(answer)
            if answer.lower() in ('q', 'й'):
                sys.exit()

    def find_new(self) -> str:
        """ Find all CSVs in the work directory. Return filename. """
        all_files = list(Path().glob('*.csv'))
        if all_files:
            print("Таблицы в текущей папке:")
            for file in all_files:
                file_option_string = f'  {all_files.index(file) + 1}. {str(file)}{fg("#444")}'
                file_size_string = f'{attr("reset")}{int(os.path.getsize(file) / 1024):,} KB'
                # Adding 15 of colored special characters.
                print(f'{file_option_string}'.ljust(self.win_with - len(file_size_string) + 15, '.'), end='')
                print(f'{file_size_string}')
            print()
            if len(all_files) == 1:
                choose = 1
            else:
                choose = Fixer.which_file(f'Выберите таблицу для обработки из 1-{len(all_files)} (Q - выход): ',
                                          len(all_files))
            print(f'{all_files[choose - 1]} ({int(os.path.getsize(all_files[choose - 1]) / 1024):,} KB)')
            print(self.win_with * '.', end='\n\n')
            return str(all_files[choose - 1])
        else:
            print(f'Для начала работы добавьте CSV в текущую папку:\n{Path.cwd()}\n')
            sys.exit(1)

    def open_csv(self):
        """ Read CSV into list. """
        for enc_read in ENCODINGS_READ:
            try:
                with open(self.filename, 'r', newline='', encoding=enc_read) as csvfile:
                    return [i for i in csv.reader(csvfile, dialect='excel', delimiter=DELIMITER) if i]
            except UnicodeDecodeError:
                continue

    @staticmethod
    def correct_number(number: str) -> str:
        """ Fix phone number into 79XXXXXXXXX format. """
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

    def run_test(self):
        for i, row in enumerate(self.all_columns):
            if len(row) < COLUMN:
                del self.all_columns[i]

    @stopwatch
    def fix(self):
        """ Main fixer. """

        self.run_test()
        for row in self.all_columns:
            number = row[self.column]
            number = Fixer.correct_number(number)
            other_columns = row[:self.column] + row[self.column + 1:]

            if (len(number) != 11 or not number.startswith('79') or not number.isdigit() or
                    re.search(r'(\d)\1{6}', number)):
                logging.warning(f"Некорректная запись: {number}")
                self.junk.append([number] + other_columns)
                continue
            if number in self.valid:
                logging.warning(f"Дубликат: {number}")
                self.dubbed.append([number] + other_columns)
            else:
                self.valid[number] = other_columns
        self.valid = [[number, *rest] for number, rest in self.valid.items()]

    def print_result(self):
        """ Print REPORT. """
        all_numbers_count = len(self.all_columns)
        junk_count = len(self.junk)
        valid_count = len(self.valid)
        Fixer.color_range(round(100 - valid_count / (all_numbers_count / 100)))  # Set result block color.
        print('[ РЕЗУЛЬТАТ ИСПРАВЛЕНИЙ ]'.center(self.win_with, '.'))
        print(f'\nБРАК: {junk_count + len(self.dubbed):,}')
        print(f'  ├ Повторы: {len(self.dubbed):,}')
        print(f'  └ Мусор: {junk_count:,}')
        print(f'\nНОМЕРА: {valid_count / all_numbers_count:.0%} ({valid_count:,}/{all_numbers_count:,})\n')
        print(''.center(self.win_with, '-'))
        print(attr("reset"))  # Reset result block color.

    @staticmethod
    def save_rows(rows, filename):
        """ Save number list in CSV file. """
        if rows:  # Save CSVs only with data.
            with open(filename, 'w', newline='', encoding=ENCODING_WRITE) as file:
                writer = csv.writer(file, dialect='excel', delimiter=DELIMITER)
                for row in rows:
                    writer.writerow(row)
            print(f'{fg("dodger_blue_3")}[CSV] {len(rows)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        """ Save all CSVs. """
        os.makedirs(self.dir_result + os.sep + self.basename, exist_ok=True)
        Fixer.save_rows(self.valid, self.dir_result + os.sep + self.basename + os.sep + self.basename + '[valid].csv')
        Fixer.save_rows(self.dubbed, self.dir_result + os.sep + self.basename + os.sep + self.basename + '[dubs].csv')
        Fixer.save_rows(self.junk, self.dir_result + os.sep + self.basename + os.sep + self.basename + '[junk].csv')

    @staticmethod
    def color_range(numb):
        """ Colorise based on stats. """
        if numb < 4:
            print(fg("#52a7563"), end='')  # green
        elif numb < 30:
            print(fg("yellow"), end='')
        elif numb < 60:
            print(fg("orange_red_1"), end='')
        else:
            print(fg("#e51c24"), end='')  # red

    def open_on_complete(self):
        path = os.path.abspath(self.dir_result + os.sep + self.basename)
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', path])
        elif platform.system() == 'Linux':
            try:
                subprocess.Popen(['xdg-open', path])
            except FileNotFoundError:
                pass

    def print_flag(self):
        """ Print flag. """
        print()
        print(bg("cornsilk_1") + fg("cornsilk_1") + 'R' * self.win_with + attr("reset"))
        print(bg("dodger_blue_3") + fg("dodger_blue_3") + 'U' * self.win_with + attr("reset"))
        print(bg("red_3a") + fg("red_3a") + 'S' * self.win_with + attr("reset"))

        self.open_on_complete()

    @staticmethod
    def clear_screen():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')


if __name__ == '__main__':
    q = ''
    while q.lower() not in ('q', 'й'):
        fixer = Fixer()
        fixer.fix()
        fixer.print_result()
        fixer.save_everything()

        make_plot(fixer.dir_result + os.sep + fixer.basename + os.sep + fixer.basename + '.png', fixer.filename,
                  len(fixer.valid), len(fixer.dubbed), len(fixer.junk))
        fixer.print_flag()
        q = input('ENTER чтобы выбрать другую таблицу (Q - выход): ')

        Fixer.clear_screen()
