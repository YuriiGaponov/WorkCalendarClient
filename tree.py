"""
Модуль tree.py: выводит структуру директории в виде дерева.

Скрипт рекурсивно обходит файловую систему от корня проекта и формирует наглядное
текстовое представление иерархии папок и файлов. Поддерживает фильтрацию элементов
и запись результата в файл.

Особенности:
    - структура начинается с имени корневой папки проекта;
    - используется визуализация с символами: '├──', '└──', '│';
    - автоматически исключаются служебные элементы;
    - возможна запись вывода в файл с кодировкой UTF‑8;
    - есть опция показа скрытых файлов.

Исключаемые элементы (всегда пропускаются):
    - сам скрипт (по имени файла);
    - папка 'venv' (виртуальное окружение);
    - файл 'structure.txt' (результат предыдущего запуска);
    - папка '.git' (репозиторий Git);
    - папка '__pycache__' (байт‑код Python).

Способы запуска:

1. Вывод в консоль (без скрытых файлов):
       $ python tree.py

2. Вывод в консоль (с показом скрытых файлов):
       $ python tree.py --hidden

3. Запись в файл structure.txt (без скрытых):
       $ python tree.py --to-file

4. Запись в файл structure.txt (с показом скрытых):
       $ python tree.py --to-file --hidden

Параметры командной строки:
    --hidden     : включает в вывод скрытые файлы (начинающиеся с '.').
    --to-file   : сохраняет результат в файл 'structure.txt' (UTF‑8).


Результат:
    При использовании --to-file скрипт выводит сообщение:
        "Структура записана в structure.txt (UTF-8)"

Обработка ошибок:
    Если к какой‑то директории нет доступа (PermissionError),
    выводится '[Доступ запрещён]' вместо её содержимого.

Пример вывода (фрагмент):
    my_project
        ├── main.py
        ├── docs/
        │   └── README.md
        └── src/
            ├── __init__.py
            └── utils.py
"""

import os

def print_tree(startpath, prefix='', script_name=None, show_hidden=False):
    # Получаем имя текущего скрипта для исключения
    if script_name is None:
        script_name = os.path.basename(__file__)


    try:
        entries = sorted(os.listdir(startpath))
    except PermissionError:
        print(f"{prefix}[Доступ запрещён]")
        return


    for i, entry in enumerate(entries):
        path = os.path.join(startpath, entry)

        # Пропускаем: сам скрипт, venv, structure.txt, .git
        if (entry == script_name or
            entry == 'venv' or
            entry == 'structure.txt' or
            entry == '.git' or
            entry == '__pycache__' or
            entry == '.pytest_cache'):
            continue

        # Скрытые файлы показываем только если show_hidden=True
        if not show_hidden and entry.startswith('.'):
            continue

        is_last = (i == len(entries) - 1)
        connector = '└── ' if is_last else '├── '
        print(f"{prefix}{connector}{entry}")

        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_tree(path, prefix + extension, script_name, show_hidden)

if __name__ == '__main__':
    import sys

    # Определяем корневую папку проекта (родительскую для скрипта)
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_name = os.path.basename(project_root)

    # Проверяем аргументы командной строки
    show_hidden = '--hidden' in sys.argv
    write_to_file = '--to-file' in sys.argv

    if write_to_file:
        with open('structure.txt', 'w', encoding='utf-8') as f:
            import io
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            # Выводим название проекта как корень структуры
            print(project_name)
            print_tree(project_root, '    ', show_hidden=show_hidden)

            output = sys.stdout.getvalue()
            f.write(output)
            sys.stdout = old_stdout
        print("Структура записана в structure.txt (UTF-8)")
    else:
        # Вывод в консоль
        print(project_name)
        print_tree(project_root, '    ', show_hidden=show_hidden)
