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
`py -m venv .venv` (Windows) или `python -m venv .venvu` (Linux/MacOS/Windows с python в PATH)
3. Активируйте виртуальную среду:
`.\.venv\Scripts\activate` (Windows) или `source ./.venvu/bin/activate` (Linux/MacOS)
4. Установите wheel:
`pip install wheel`
5. Установите зависимости:
`pip install -r requirements.txt`

6. Переместите использованные таблицы в папку Used.*
7. Поместите нужную для анализа файл-таблицу в рабочую папку (папка, из которой запускаются скрипты).

### Требования к таблицам

* Тип файла: MS Excel CSV (разделитель: точка с запятой)
* Номера находятся в 1 колонке («А»), для FIXER выбирается интерактивно
* Формат 79XXXXXXXXX, для FIXER — любой формат

_Для валидации файлов рекомендуется обработать их через FIXER._
***
### Использование
По умолчанию в Windows установлен запрет на исполнение скриптов PowerShell.
Перед первым запуском PowerShell-скрипта необходимо установить политику исполнения:
1. Откройте PowerShell с правами Администратора.
2. Введите команду `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned CurrentUser` ([подробнее](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)).
3. В `Properties` любого файла с расширением `ps1` изменить `Open with:` на `Windows PowerShell` (C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe).

Запустить модуль `Fixer` или `Comparer` в зависимости от задачи, выбрать файл из предложенных
(предлагаются файлы из текущей рабочей папки).
Разрешения для разных ОС:
* .ps1 - Windows (PowerShell Script)
* .sh - Linux (Shell Script)
* .command - MacOS (необходимо разрешить исполнение `chmod +x Fixer.command` и `chmod +x Comparer.command`)

***
### Выбор режима логирования (отображение большого количества логов существенно замедляет обработку)
В файле настроек `config.py` в строке `LOG_MODE = logging.<MODE_NAME>` поменять режим на желаемый уровень.
В порядке уменьшения количества логов уровни бывают:
1. `INFO` - исправления + `WARNING`
2. `WARNING` - дубли и мусор
3. `disable()` - отключает логи

Пример: `LOG_MODE = logging.INFO`


### Выбор кодировки на запись
В файле настроек `config.py` указать в строке: `ENCODING_WRITE = <encoding>` нужную кодировку.


### Ширина вывода строк в терминале
Как настроить:

1. _Настройка ширины вывода строк в CMD:_
`сmd.exe` > `Properties` > `Layout` > `Window Size` > `Width`

2. _Настройка ширины вывода строк в терминале:_
В `config.py` установить значение `WIN_WIDTH` меньше ширины CMD на 1.
