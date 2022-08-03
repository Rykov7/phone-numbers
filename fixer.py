""" fix_numbers.py - Приводит телефонные номера к формату 79XXXXXXXX """
import csv
import os
import logging
from pathlib import Path
from colored import bg, fg, attr
from config import LOG_MODE

# Формат файла (сделать вручную, если не соответствует):
# 1) Формат: CSV
# 2) Номера находятся в колонке А
# 3) Нет заголовков (1 строка содержит данные, а не название колонки)""")


logging.basicConfig(level=LOG_MODE, format='%(levelname)s - %(message)s')
TRANSLATION = str.maketrans('', '', '() -,.-+')  # Из номеров удаляются перечисленные символы.


class Analyzer:
    def __init__(self):
        self.win_with = 79
        self.greeting()
        self.error_numbers, self.dubbed, self.valid_numbers = [], [], []
        self.filename = self.find_new()
        self.all_numbers = self.open_csv()
        self.numbers = []
        self.result_dir = self.filename[:-4] + '_[RESULT]'

    def greeting(self):
        print('ИСПРАВЛЯТОР'.rjust(self.win_with))
        print('Приводит телефонные номера к формату 79XXXXXXXX'.rjust(self.win_with))
        print()

    @staticmethod
    def _which_file(question, allow_range):
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
        all_files = list(Path().glob('*.csv'))

        print("CSV в текущей директории: ")
        for file in all_files:
            print(f'\t{all_files.index(file)+1} - {str(file)}')
        print()
        choose = self._which_file(f'Выберите файл для обработки (1-{len(all_files)}): ', len(all_files))
        print()
        return str(all_files[choose-1])

    def open_csv(self):
        with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
            return [i[0] for i in list(csv.reader(csvfile)) if i]

    def analyze(self):
        for number in self.all_numbers:
            if not number.isdigit():
                logging.debug(f'{fg("red")}{number}{attr("reset")} удаление лишних символов. ')
                number = number.translate(TRANSLATION)  # Убираем нецифровые символы.
            if number.startswith('8') and len(number) == 11:
                logging.debug(f'{fg("red")}{number[:1]}{attr("reset")}{number[1:]} исправление 8 на 7.')
                number = '7' + number[1:]
            elif number.startswith('9') and len(number) == 10:
                logging.debug(f'{number} добавляю приставку 7.')
                number = f'7' + number
            elif len(number) < 10:
                self.error_numbers.append(number)
                logging.info(f"{fg('red')}Невалидный номер {number}{attr('reset')}")
                continue
            self.numbers.append(number)
            if self.numbers.count(number) >= 2:
                logging.info(f"{fg('red')}Дубликат! {number}{attr('reset')}")
                self.dubbed.append(number)

    def result(self):
        self.valid_numbers = set(self.numbers)
        print()
        print('[ ОТЧЁТ ]'.center(100, '-'))
        total = len(self.all_numbers)
        errors = len(self.error_numbers)         # Некорректные номера
        valid_num = len(self.valid_numbers)      # Валидные уникальные номера

        print(f'\nИз {total} удалено {errors + len(self.dubbed)}  шт.')
        print(f'  ├ некорректных: {errors}')
        print(f'  ├ дубликатов: {len(self.dubbed)}')

        print(f'\nИТОГ')
        print(f'  └ КАЧЕСТВО: {round(valid_num/(total/100), 2)}% ({valid_num})\n')

    @staticmethod
    def _save_numbers(numbs, filename):
        if numbs:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for numb in numbs:
                    writer.writerow([numb])
            print(f'{bg("blue")}[СОХРАНЕНО] {len(numbs)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.valid_numbers, self.result_dir + os.sep + self.filename[:-4] + '[valid].csv')
        self._save_numbers(set(self.dubbed), self.result_dir + os.sep + self.filename[:-4] + '[dubbed].csv')
        self._save_numbers(self.error_numbers, self.result_dir + os.sep + self.filename[:-4] + '[errs].csv')


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.analyze()
    analyzer.result()
    analyzer.save_everything()

