""" fixer.py - Приводит телефонные номера к формату 79XXXXXXXXX """
import csv
import os
import logging
from pathlib import Path
from colored import bg, fg, attr
from config import LOG_MODE, WIN_WIDTH
from pie import make_plot

# Формат файла (сделать вручную, если не соответствует):
# 1) Формат: CSV
# 2) Номера находятся в колонке А
# 3) Нет заголовков (1 строка содержит данные, а не название колонки)


logging.basicConfig(level=LOG_MODE, format=f'{fg("yellow")}%(message)s{attr("reset")}')
TRANSLATION = str.maketrans('', '', '() -,.-+')  # Из номеров удаляются перечисленные символы.


class Fixer:
    """ Исправлятор. """
    def __init__(self):
        self.win_with = WIN_WIDTH
        self.greeting()
        self.error_numbers, self.dubbed, self.valid_numbers = [], [], []
        self.filename = self.find_new()
        self.all_numbers = self.open_csv()
        self.numbers = []
        self.result_dir = '[FIXER]'

    def greeting(self):
        """ Приветствие программы. """
        print('ИСПРАВЛЯТОР'.rjust(self.win_with))
        print('Приводит телефонные номера к формату 79XXXXXXXXX'.rjust(self.win_with))
        print()

    @staticmethod
    def _which_file(question, allow_range):
        """ Проверяет выбранный номер файла на валидность. """
        answer = ''
        while not answer.isdigit():
            answer = input(question)
            if answer.isdigit():
                if int(answer) in range(1, allow_range+1):
                    return int(answer)
                else:
                    answer = ''
            else:
                pass

    def find_new(self):
        """ Ищет все CSV в текущей директории. """
        all_files = list(Path().glob('*.csv'))

        print("CSV в текущей директории: ")
        for file in all_files:
            print(f'\t{all_files.index(file)+1} - {str(file)}')
        print()
        choose = self._which_file(f'Выберите файл для обработки (1-{len(all_files)}): ', len(all_files))
        print()
        return str(all_files[choose-1])

    def open_csv(self):
        """ Открывает CSV """
        with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
            return [i[0] for i in list(csv.reader(csvfile)) if i]

    def fix(self):
        """ Анализирует и исправляет номера. """
        for number in self.all_numbers:
            if not number.isdigit():
                logging.info(f'{number} удалил лишние символы. ')
                number = number.translate(TRANSLATION)  # Убираем нецифровые символы.
            if number.startswith('8') and len(number) == 11:
                logging.info(f'{number} исправил 8 на 7.')
                number = '7' + number[1:]
            elif number.startswith('9') and len(number) == 10:
                logging.info(f'{number} добавил 7 перед номером.')
                number = f'7' + number
            elif len(number) < 10:
                self.error_numbers.append(number)
                logging.warning(f"Нашёл некорректную запись {number}")
                continue
            self.numbers.append(number)
            if self.numbers.count(number) >= 2:
                logging.warning(f"Нашёл дубликат {number}")
                self.dubbed.append(number)

    def result(self):
        """ Выводит ОТЧЁТ со статистикой в текстовом виде. """
        self.valid_numbers = set(self.numbers)

        total = len(self.all_numbers)
        errors = len(self.error_numbers)         # Некорректные номера
        valid_num = len(self.valid_numbers)      # Валидные уникальные номера
        print()
        self.color_range(round(100 - valid_num/(total/100)))
        print('[ ОТЧЁТ ]'.center(self.win_with, '-'))

        print(f'\nИз {total} удалено {errors + len(self.dubbed)}  шт.')
        print(f'  ├ некорректных: {errors}')
        print(f'  └ дубликатов: {len(self.dubbed)}')

        print(f'\nИТОГ')
        print(f'  └ КАЧЕСТВО: {int(valid_num/(total/100))}% ({valid_num}){attr("reset")}\n')

    @staticmethod
    def _save_numbers(numbs, filename):
        """ Сохраняет список номеров в файл. """
        if numbs:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for numb in numbs:
                    writer.writerow([numb])
            print(f'{bg("blue")}[СОХРАНЕНО] {len(numbs)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        """ Сохраняет все файлы. """
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.valid_numbers, self.result_dir + os.sep + self.filename[:-4] + '[valid].csv')
        self._save_numbers(set(self.dubbed), self.result_dir + os.sep + self.filename[:-4] + '[dubbed].csv')
        self._save_numbers(self.error_numbers, self.result_dir + os.sep + self.filename[:-4] + '[errs].csv')

    @staticmethod
    def color_range(numb):
        """ Определяет цвет текста, в зависимости от процента совпадений. """
        if numb < 5:
            print(fg("green"), end='')
        elif numb < 20:
            print(fg("yellow"), end='')
        elif numb < 50:
            print(fg("orange_red_1"), end='')
        else:
            print(fg("red"), end='')

    def russian_flag(self):
        """ Печатает флаг России. """
        print()
        print(bg("white") + fg("white") + 'R' * self.win_with + attr("reset"))
        print(bg("blue") + fg("blue") + 'U' * self.win_with + attr("reset"))
        print(bg("red") + fg("red") + 'S' * self.win_with + attr("reset"))


if __name__ == '__main__':
    fixer = Fixer()
    fixer.fix()
    fixer.result()
    fixer.save_everything()
    fixer.russian_flag()

    # Сохраняет изображение с графиком.
    make_plot(fixer.result_dir + os.sep + fixer.filename[:-4], fixer.filename,
              len(fixer.valid_numbers), len(fixer.dubbed), len(fixer.error_numbers))
