### README.MD
###### Автор: t.me/Rykov7
***

### Описание
1. `Fixer` исправляет номера в таблице. На выходе в папке `[FIXER]` создаёт новые таблицы:
   * `[valid]` - номера 
   * `[dubs]` - дубли
   * `[junk]` - мусор

2. `Comparer` сравнивает одну таблицу с номерами со всеми остальными из Used. На выходе в папке `[COMPARER]` создаёт таблицы:
   * `[UNIQUE]` - уникальные
   * `[OVERLAP]` - пересечения

В обеих программах сохраняется график с результатами в PNG.

### Системные требования:
1. Python 3.8 или выше
2. Windows/MacOS/Linux

### Установка:
1. В терминале перейдите в папку программой: `ПКМ` > `Open in Terminal` (Windows), `cd [ПУТЬ]` (MacOS/Linux)
2. Создайте виртуальную среду:
   * Windows: `py -m venv .venv`
   * MacOS/Linux `python -m venv .venvu` (или `python3`) в зависимости от вашей системы (`ls /bin | grep ^python`).
3. Активируйте виртуальную среду:
`.\.venv\Scripts\activate` (Windows) или `source ./.venvu/bin/activate` (Linux/MacOS)
4. Установите wheel:
`pip install wheel`
5. Установите зависимости:
`pip install -r requirements.txt`
6. Переместите использованные таблицы в папку Used.
7. Поместите нужную для работы файл-таблицу в рабочую папку (папка, из которой запускаются скрипты).
8. Разрешите исполнение скриптов:
   * MacOS: разрешите исполнение файлов `chmod +x Fixer.command` и `chmod +x Comparer.command`
   * Windows: установите политику исполнения:
     1. Откройте PowerShell с правами Администратора.
     2. Введите команду `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned CurrentUser` ([подробнее](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)).
     3. В `Properties` любого файла с расширением `ps1` измените `Open with:` на `Windows PowerShell` (C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe).

### Требования к таблицам

* Тип файла: MS Excel CSV (разделитель: точка с запятой)
* Номера находятся в 1 колонке («А»), для FIXER выбирается интерактивно
* Формат 79XXXXXXXXX, для FIXER — любой формат

***
### Использование

Запустите модуль `Fixer` или `Comparer` в зависимости от задачи, выбрать файл из предложенных
(предлагаются файлы из текущей рабочей папки).
Разрешения для разных ОС:
* .ps1 - Windows (PowerShell Script)
* .command - MacOS (Mac Script), Linux

***
### Выбор режима логирования (отображение большого количества логов существенно замедляет обработку)
В файле настроек `config.py` в строке `LOG_MODE = logging.<MODE_NAME>` поменяйте уровень на желаемый.
В порядке уменьшения количества логов уровни бывают:
1. `INFO` - исправления + `WARNING`
2. `WARNING` - дубли и мусор
3. `disable()` - отключает логи

Пример: `LOG_MODE = logging.INFO`


### Выбор кодировки на запись
В файле настроек `config.py` укажите в строке: `ENCODING_WRITE = <encoding>` нужную кодировку.


### Как настроить ширину вывода строк в терминале
В `config.py` установите значение `WIN_WIDTH` меньше ширины CMD на 1.
