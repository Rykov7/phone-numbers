""" comparison.py - Сравнивает новую таблицу номеров со старыми. """

import os
from pathlib import Path
import csv
from colored import bg, attr
from fix_numbers import Analyzer




def greeting():
    print('comparison.py'.rjust(100))
    print('Сравнивает новую таблицу со старыми'.rjust(100))
    print()


def find_used():
    used_tables = []
    for folder_name, subfolders, filenames in os.walk(Path('used')):
        for file in Path(folder_name).glob('*.csv'):
            used_tables.append(file)
    return used_tables


def open_new_table():
    with open('Выгрузка_БФЛ_Тест_1_[VALID].csv', 'r', newline='') as csvfile:
        return list(csv.reader(csvfile))


def comparison():
    counter_all_dubbed = 0
    for used_table in find_used():
        print(f"\nТАБЛИЦА: {used_table}")
        dubbed = []
        with open(used_table, 'r', newline='') as csvfile:
            used_numbers = list(csv.reader(csvfile))

        for used_number in used_numbers:
            if used_number in open_new_table():
                print(f'{bg("red")}{used_number[0]} уже есть в старой таблице!{attr("reset")}')
                dubbed.append(used_number)
                counter_all_dubbed += 1

        dubbed_count = len(dubbed)

        print()
        print('[ ОТЧЁТ ]'.center(100, '-'))
        print(f'Пересечений с {used_table}: {dubbed_count} ')
        print(f'СОВПАДЕНИЕ С ТЕКУЩЕЙ ТАБЛИЦЕЙ: '
              f'{round(100 - (len(open_new_table())-dubbed_count)/(len(open_new_table())/100), 2)}%')
        print()
    return counter_all_dubbed


def overall():
    print(f'Пересечений со всеми: {comparison()} ')
    print(f'ОБЩАЯ УНИКАЛЬНОСТЬ: {round((len(open_new_table())-comparison())/(len(open_new_table())/100), 2)}%')


if __name__ == '__main__':
    comparison()
    input()