import os
from laba import Greenhouse
from functions import init_foo

if __name__ == '__main__':

    mode = (input('Выберите режим: [1]Считывать комнады с терминала [2]Считывать команды с файла\nВведите команду: '))
    if not mode.isdigit():
        print('Неверный формат команды')
        exit(0)
    else: mode = int(mode)

    file_name = ''
    files_commands = []
    file_output = ''

    if mode == 2:
        file_name = input('Введите файл для ивзлечения данных: ')
        file_name = 'tests\\' + file_name

        if not os.path.exists(file_name): 
            print("Файл не существует.")
            exit(0)
        else:
            file_name = open(file_name, 'r', encoding="utf-8")

            file_output = input('Введите файл для вывода данных: ')
            file_output = 'tests\\output\\' + file_output
            file_output = open(file_output, 'w', encoding="utf-8")

            files_commands = file_name.read().split('\n')
    elif mode != 1: 
        print('Неизвестная команда.')
        exit(0)
    
    if mode == 1: print('-' * 100)
    greenhouse = Greenhouse()
    code = -1
    while code != 0:

        command = ''
        if mode == 2:
            command = files_commands[0]
            file_output.write('-' * 100) 
            file_output.write(f'\nБыла введена команда: {command}\n')

            del files_commands[0]
        else:
            command = input('Введите команду: ')

        code, greenhouse, output = init_foo(command, greenhouse)

        if mode == 1: print(f'{output}')
        if mode == 2:
            file_output.write(f'\n{output}\n')
        if code != 0 and mode == 1: print('-' * 100)
