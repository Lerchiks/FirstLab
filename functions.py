from laba import (Greenhouse, Orchid, AppleTree, Time)
from laba import type_plant

default_time = lambda x: Time(int(x.split(':')[0]) * 60 + int(x.split(':')[1]))


def init_foo(command: str, greenhouse: Greenhouse) -> tuple[int, Greenhouse, str]:

    command = command.split(' ')
    cmd: int = int(command[0]) if command[0].isdigit() else -1
    output = ''

    if cmd == 0:
        output = 'Работа завершена.'
        return 0, greenhouse, output
    
    if cmd == 1:
        if ':' in command[1]: output += greenhouse.time_change(default_time(command[1]))
        else: output += 'Неверный формал ввода времени.'
        return 1, greenhouse, output
    
    if cmd == 2:
        new_plant = 'Err'

        if command[1] == 'Орхидея': new_plant = Orchid(command[2], int(command[3]), int(command[4]), greenhouse.time_exists)
        elif command[1] == 'Яблоня': new_plant = AppleTree(command[2], int(command[3]), int(command[4]), greenhouse.time_exists)
        else: return 2, greenhouse, 'Неизвестное растение.'

        for plant in greenhouse.plants:
            if plant.name == command[2]: 
                output += (f'В оранжерее уже есть растение с таким именем[{type_plant(plant)} {plant.name}].')
                new_plant = 'Err'

        if new_plant != 'Err':
            greenhouse += new_plant
            output += (f'Успешно добавлена {type_plant(new_plant)} <<{new_plant.name}>>')

        return 2, greenhouse, output
    
    if cmd == 3:
        return 3, greenhouse, greenhouse.water_the_plant(command[1], int(command[2]))
    
    if cmd == 4:
        return 4, greenhouse, greenhouse.sun_the_plant(command[1], int(command[2]))
    
    if cmd == 5:
        if greenhouse[command[1]] in greenhouse.plants:
            output += f'Была удалена {type_plant(greenhouse[command[1]])} {greenhouse[command[1]].name}'
            del greenhouse[command[1]]
        else: output += 'Такого растения нет в оранжерее.\n'
        return 5, greenhouse, output
    
    if cmd == 6:
        output += f'{greenhouse[command[1]]}'
        return 6, greenhouse, output
    
    if cmd == 7:
        output += f'{greenhouse}'
        return 7, greenhouse, output
    
    if cmd not in [0,1,2,3,4,5,6,7]:
        output += 'Неизвестная команда\n'
        return -1, greenhouse, output