""" fix_numbers.py - Приводит телефонные номера к формату 79XXXXXXXX """
import csv
import os
import logging
from pathlib import Path
from colored import bg, attr
from config import LOG_MODE

# Формат файла (сделать вручную, если не соответствует):
# 1) Формат: CSV
# 2) Номера находятся в колонке А
# 3) Нет заголовков (1 строка содержит данные, а не название колонки)""")


logging.basicConfig(level=LOG_MODE, format='%(levelname)s - %(message)s')
TRANSLATION = str.maketrans('', '', '() -,.-+')  # Из номеров удаляются перечисленные символы.


class Analyzer:
    def __init__(self):
        self.win_with = 100
        self.greeting()
        self.empty_counter = 0
        self.error_numbers, self.dubbed, self.valid_numbers = [], [], []
        self.filename = self.find_new()
        self.all_numbers = self.open_csv()
        self.numbers = []
        self.result_dir = self.filename[:-4] + '_[RESULT]'

    def greeting(self):
        print('fix_numbers.py'.rjust(self.win_with))
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
            print(f'{all_files.index(file)+1} - {str(file)}')

        choose = self._which_file(f'Какой файл проверять? (1-{len(all_files)}): ', len(all_files))
        print()
        return str(all_files[choose-1])

    def open_csv(self):
        with open(self.filename, 'r', newline='') as csvfile:
            return list(csv.reader(csvfile))  # Читаем все номера из файла.

    def analyze(self):
        for row in self.all_numbers:
            if row:
                number = row[0]
            else:
                logging.debug(f'{bg("red")}Пустая строка!{attr("reset")}')
                self.empty_counter += 1
                continue
            if not number.isdigit():
                logging.debug(f'{bg("red")}{number}{attr("reset")} удаление лишних символов. ')
                number = number.translate(TRANSLATION)  # Убираем нецифровые символы.
            if number.startswith('8') and len(number) == 11:
                logging.debug(f'{bg("red")}{number[:1]}{attr("reset")}{number[1:]} исправление 8 на 7.')
                number = '7' + number[1:]
            elif number.startswith('9') and len(number) == 10:
                logging.debug(f'{number} добавляю приставку 7.')
                number = f'7' + number

            elif len(number) < 10:
                self.error_numbers.append(number)
                logging.info(f"{bg('red')}Невалидный номер {number}{attr('reset')}")
                continue
            self.numbers.append(number)
            if self.numbers.count(number) >= 2:
                logging.info(f"{bg('red')}Дубликат! {number}{attr('reset')}")
                self.dubbed.append(number)

    def result(self):
        self.valid_numbers = set(self.numbers)
        print()
        print('[ ОТЧЁТ ]'.center(100, '-'))
        total = len(self.all_numbers)
        errors = len(self.error_numbers)         # Некорректные номера
        valid_num = len(self.valid_numbers)      # Валидные уникальные номера

        print(f'\nИз {total} удалено {errors + len(self.dubbed) + self.empty_counter} шт.')
        print(f'  ├ некорректных: {errors}')
        print(f'  ├ дубликатов: {len(self.dubbed)}')
        print(f'  └ пустых строк: {self.empty_counter}')

        print(f'\nИТОГ')
        print(f'  └ КАЧЕСТВО: {round(valid_num/(total/100), 2)}% ({valid_num})\n')

    @staticmethod
    def _save_numbers(numbs, filename):
        if numbs:
            with open(filename, 'w', newline='') as fixed_file:
                writer = csv.writer(fixed_file)
                for numb in numbs:
                    writer.writerow([numb])
            print(f'{bg("blue")}[СОХРАНЕНО] {len(numbs)} шт. в файле {filename}{attr("reset")}')

    def save_everything(self):
        os.makedirs(self.result_dir, exist_ok=True)
        self._save_numbers(self.valid_numbers, self.result_dir + os.sep + self.filename[:-4] + '_[VALID].csv')
        self._save_numbers(set(self.dubbed), self.result_dir + os.sep + self.filename[:-4] + '_[DUBBED].csv')
        self._save_numbers(self.error_numbers, self.result_dir + os.sep + self.filename[:-4] + '_[ERRS].csv')


if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.analyze()
    analyzer.result()
    analyzer.save_everything()

    input()
