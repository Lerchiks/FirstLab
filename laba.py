from __future__ import annotations
import random

default_hrs = lambda x: str(x // 60) if len(str(x // 60)) >= 2  else '0' + str(x // 60)
default_mns = lambda x: str(x % 60) if len(str(x % 60)) >= 2 else '0' + str(x % 60)
default_time = lambda x: Time(int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

catch = False

def timer(time: Time):
    if time // 60 != 0 and time % 60 != 0:
        return str(time // 60) + ' часов и ' + str(time % 60) + ' минут'
    if time // 60 == 0 and time % 60 != 0:
        return str(time % 60) + ' минут'
    if time // 60 != 0 and time % 60 == 0:
        return str(time // 60) + ' часов'
    return 'нисколько' 

class Time:

    def __init__(self, time: int = 0): self.time = time
    def __add__(self, other): return Time(self.time + other.time) if type(other) == Time else Time(self.time + other)
    def __mul__(self, other): return Time(self.time * other.time) if type(other) == Time else Time(self.time * other)
    def __sub__(self, other): return Time(self.time - other.time) if type(other) == Time else Time(self.time - other)
    def __floordiv__(self, other): return Time(self.time // other.time) if type(other) == Time else Time(self.time // other)
    def __mod__(self, other: Time): return Time(self.time % other.time) if type(other) == Time else Time(self.time % other)
    def __eq__(self, other): return self.time == other.time if type(other) == Time else self.time == other
    def __ne__(self, other): return not self == other
    def __repr__(self): return default_hrs(self.time) + ':' + default_mns(self.time)
    def __str__(self): return str(self.time)
    def __ge__(self, other): return self.time >= other.time if type(other) == Time else self.time >= other
    def __lt__(self, other): return self.time < other.time if type(other) == Time else self.time < other
    def __gt__(self, other): return self.time > other.time if type(other) == Time else self.time > other

def type_plant(plant):
    '''При реализации Нового дочернего класса Растений, необходимо только добавить новый тип в данный журнал'''
    if type(plant) == Orchid: return 'Орхидея'
    if type(plant) == AppleTree: return 'Яблоня'
    else: return 'Неизвестное растение'

class Greenhouse:

    def __init__(self, time_exists: Time = 0):
        self.time_exists: Time = Time(time_exists)
        self.plants = []
        self.apples = 0

    def sort_plants(self):
        '''Метод нужен для отсортированного вывода инфорамции о растениях по категориям.
          Отдельно выводится информация по всем Растениям группы А, затем группы Б и тд'''
        copy_plants = self.plants.copy()
        copy_plants.pop(0)

        if len(self.plants) > 0: new_list = [self.plants[0]]
        catch_type = type(self.plants[0])
        index = 0
        while len(copy_plants) > 0:
            if any(isinstance(plant, catch_type) for plant in copy_plants):
                if type(copy_plants[index]) == catch_type:
                    new_list.append(copy_plants[index])
                    copy_plants.pop(index)
                else: index += 1
            else:
                catch_type = type(copy_plants[0])
                index = 0
                new_list.append(copy_plants[index])
                copy_plants.pop(0)
        self.plants = new_list

    def time_change(self, new_time: Time) -> str:
        '''Возвращает логи событий'''
        global catch
        logs = ''
        old_data: Time = self.time_exists
        plant_grown  = False
        logs += (f'Время изменилось с {default_hrs(old_data)}:{default_mns(old_data)}' 
              f' на {default_hrs(self.time_exists + new_time)}:{default_mns(self.time_exists + new_time)} - прошло: '
              f'{timer(new_time)}')
        
        if len(self.plants) == 0: logs += ('\nОранжерея пуста.') 
        else:
            
            for plant in self.plants:
                if not plant.death:
                    old_plant_health = plant.health
                    time_limit = plant.GROW_TIME
                    svd, usd = False, False
                    plant_grown = False
                    logs += ( '\n' + '☆' * 70)
                    logs += (f'\n {' ' * 35} ***Журнал событий {type_plant(plant)} {plant.name}***\n')
                    # Пока растение живое и может расти -> растет
                    while not plant.death and (plant.life + time_limit <= Time(old_data) - (Time(self.time_exists) - plant.life) + new_time or
                                            (plant.life - ((plant.life // time_limit) * time_limit) + new_time >= time_limit and
                                            plant.life + new_time <= Time(old_data) - (Time(self.time_exists) - plant.life) + new_time)) : 
                        
                        usd = True
                        catch = True
                        if plant.grow_status == 100: 
                            plant_grown = True
                            
                        old_plant_life = plant.life
                        logs += plant.to_grow() # добавили 20 минут остальные позже
                        if new_time >= time_limit: self.time_exists += time_limit
                        else: 
                            plant.life = plant.life - time_limit + (new_time % time_limit) 
                            svd = True
                            self.time_exists += new_time
                            
                        logs += self.tend_to_plants(plant)
                        plant.health_research(plant.life - old_plant_life) #Проверка на здоровье
                        evol = plant.evolution(self.time_exists) # выходные данные -> [apples, logs]
                        
                        if type(plant) == AppleTree: self.apples += evol[0]
                        logs += evol[1]

                        if not plant_grown: logs += (f'\n[{default_hrs(self.time_exists)}:{default_mns(self.time_exists)}]'
                                                f'{type_plant(plant)} {plant.name} подросла! [{plant.grow_status}/100]')

                    if new_time - ((new_time // time_limit) * time_limit) < time_limit and not svd: 
                        old_plant_life = plant.life
                        plant.life += (new_time % time_limit)
                        plant.health_research(plant.life - old_plant_life)
                        evol = plant.evolution(self.time_exists) # выходные данные -> [apples, logs]
                        
                        if type(plant) == AppleTree: self.apples += evol[0]
                        logs += evol[1]

                    if not usd:
                        logs += self.tend_to_plants(plant)
                        
                        if type(plant) == AppleTree: self.apples += evol[0]
                        logs += evol[1]

                    if plant.bad != None and not plant.death:
                        logs += (f'\n(ᗒᗣᗕ) {type_plant(plant)} {plant.name} болеет. [{plant.get_health_status()}] '
                                                                    f'Сколько времени болеет: {default_hrs(plant.bad)}:{default_mns(plant.bad)}')
                    if plant.death: logs += f'\n{type_plant(plant)} {plant.name} умирает от болезни'

                    if old_plant_health < plant.health:
                        catch = True
                        logs += f'\n{type_plant(plant)} {plant.name} выздоравливает! [{plant.get_health_status()}]'

                    self.time_exists -= ((new_time // time_limit) * time_limit)
                    if usd and ((new_time // time_limit) * time_limit) == 0: self.time_exists -= new_time
                    if plant.death: self.time_exists = old_data
                    if not catch: logs += (f'{' ' * 27}Ничего интересненького не происходило **Звук сверчков**')
                    catch = False

        self.time_exists += new_time
        return logs
        
    def tend_to_plants(self, plant: Plant) -> str: #уход за растениями
        '''
        при наличии ошибки в параметрах и при часовом диапозоне помогаем растению.
        '''
        global catch
        logs = ''
        used = [False, False]
        old_data_water = plant.water
        old_data_sun = plant.sun

        if plant.saved == None or (plant.saved + 60) <= self.time_exists and not plant.death:
            if plant.catch_err()[0] == 1 and plant.water <= plant.min_water:
                plant.saved = self.time_exists
                plant.water = plant.max_water - 1
                used[0] = True
            if plant.catch_err()[1] == 1 and plant.sun <= plant.min_sun:
                plant.saved = self.time_exists
                plant.sun = plant.max_sun - 1
                used[1] = True

        if not used[0] and not used[1]:
            if plant.catch_err()[0] and plant.catch_err()[2] != 1:
                catch = True
                logs += (f'\n[{default_hrs(self.time_exists)}:{default_mns(self.time_exists)}]{type_plant(plant)} {plant.name} имеет критические показатели воды.')
            if plant.catch_err()[1] and plant.catch_err()[2] != 1: 
                catch = True
                logs += (f'\n[{default_hrs(self.time_exists)}:{default_mns(self.time_exists)}]{type_plant(plant)} {plant.name} имеет критические показатели света.')
        else:
            if used[0]: 
                catch = True
                logs += (f'\n{' ' * 50}[{default_hrs(self.time_exists)}:{default_mns(self.time_exists)}]\n')
                logs += (f'Умная Оранжерея полила {type_plant(plant)} {plant.name}, чтобы избежать критического показателя Воды {old_data_water} -> Воды {plant.water}.\n')
            if used[1]: 
                catch = True
                logs += (f'\n{' ' * 50}[{default_hrs(self.time_exists)}:{default_mns(self.time_exists)}]\n')
                logs += (f'Умная Оранжерея осветила {type_plant(plant)} {plant.name}, чтобы избежать критического показателя Света {old_data_sun} -> Свет {plant.sun}.\n')
        
        return logs

    def water_the_plant(self, name, value: int) -> str:
        found = False
        logs = ''
        for plant in (self.plants):
            if plant.name == name:
                plant.water += value
                logs += (f'Полита {type_plant(plant)} {plant.name}.\n[{plant.water}/{plant.max_water}]')
                found = True
        if not found:
            logs += 'Такого растения в оранжерее нет.\n'
        return logs
              
    def sun_the_plant(self, name, value: int) -> str:
        found = False
        logs = ''
        for plant in (self.plants):
            if plant.name == name:
                plant.sun += value
                logs += (f'Освещена {type_plant(plant)} {plant.name}.\n[{plant.sun}/{plant.max_sun}]')
                found = True
        if not found:
            logs += 'Такого растения в оранжерее нет.\n'
        return logs
    
    def __add__(self, other): 
        if type_plant(other) != 'Неизвестное растение':
            self.plants.append(other)
            self.sort_plants()
        return self
    
    def __getitem__(self, name):
        found = False
        if type(name) == str:
            for plant in (self.plants):
                if plant.name == name: return plant
        if not found: return 'Такого растения в оранжерее нет.\n'
        if type(name) == int:
            return self.plants[name]
        return 'Ошибка'
    
    def __delitem__(self, name: str):
        found = False
        logs = ''
        for plant in (self.plants):
            if plant.name == name:
                logs += f'Была удалена {type_plant(plant)} {plant.name}\n'
                index = self.plants.index(plant)
                self.plants.pop(index)
                found = True
        if not found: logs += 'Такого растения в оранжерее нет.\n'
        return logs
    
    def __repr__(self):
        result = f'Всего растений: {len(self.plants)}\n'
        result += f'Время существования оранжереи: {default_hrs(self.time_exists)}:{default_mns(self.time_exists)}\n'
        if self.apples > 0: result += f'Всего было собрано {self.apples} яблок\n'
        result += '\n' + '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧' + '\n'

        if len(self.plants) > 0:
            catch_type = type(self.plants[0])
            result += f'\n[Информация по {type_plant(self.plants[0])}м]:\n' + '#' * 10 + '     ' + '#' * 10
            for plant in self.plants:
                if catch_type == type(plant):
                    result += '\n' + '^' * 20 + '\n' +  f'{plant}'  
                else:
                    catch_type = type(plant)
                    result += '\n' + '*' * 20 + '\n'
                    result += f'[Информация по {type_plant(plant)}м]:\n' + '#' * 10 + '     ' + '#' * 10+ f'\n{plant}'
        else:
            result += 'В оранжерее отсутствуют растения'
        return result

class Plant: 
    
    def __init__(self, name: str, water: int, sun: int, time):
        self.name, self.water, self.sun, self.life_time = name, water, sun, Time(time)
        self.health = 3 
        self.grow_status = 0

        self.life = Time(0)
        self.catch_grow = Time(0)

        self.good, self.bad = None, None
        self.saved, self.death = None, None
        self.health_research(time)

    def catch_err(self):

        result = [0,0,0]
        if not (self.min_water < self.water < self.max_water and (self.health != 0)): result[0] = 1
        if not (self.min_sun < self.sun < self.max_sun and (self.health != 0)): result[1] = 1

        if self.health <= 0: result[2] = 1
        return result

    def health_research(self, time: Time):
            errors = self.catch_err()
            if not self.death:
                # каждые 30 минут состояние ухудшается
                if self.bad == None and (1 in errors):
                    if self.good == None: self.health -= 1 
                    self.good = None# если показатели ухудшились отключаем таймер о хорошем состоянии
                    self.bad = Time(0) #запускаем таймер в 30 минут
                elif self.bad != None and (1 in errors):
                    self.good = None # если показатели ухудшились отключаем таймер о хорошем состоянии
                    self.bad += time
                    if self.bad >= 30:
                        self.health -= 1
                        self.bad -= 30
                # Каждые 90 минут состояние стабилизиуертся
                if self.good == None and not(1 in errors) and self.health < 3:
                    self.bad = None
                    self.good = Time(0)
                elif self.good != None and not(1 in errors) and self.health < 3:
                    self.bad = None
                    self.good += time
                    if self.good >= 90:
                        self.health += 1
                        if self.health < 3: self.good = Time(0)
                        else: self.good = None
            self.get_health_status()

    def to_grow(self):
        logs = ''
        if not self.death:
            self.grow_status += self.GROW_CHANGE
            if self.grow_status > 100: self.grow_status = 100
            self.water -= self.WATER_WASTE
            if self.water < 0: self.water = 0
            self.sun -= self.SUN_WASTE
            if self.sun < 0: self.sun = 0

            self.life += self.GROW_TIME
            self.catch_grow += self.GROW_TIME
        else:
            logs += (f'{type_plant(self)} больше не может расти. Статус: МЕРТВО')
        return logs

    def get_health_status(self):
        if self.health == 3: return 'Здоровое'
        if self.health == 2: return 'Легкая болезнь'
        if self.health == 1: return 'Тяжелая болезнь'
        else:
            self.death = True 
            return 'Мертво'

    def __repr__(self):
        string = (
                f'Статистика по <<{self.name}>>:\n'
                f'Тип: {type_plant(self)}\n'
                f'Вода: {self.min_water} < {self.water} < {self.max_water}\n'
                f'Свет: {self.min_sun} < {self.sun} < {self.max_sun}\n'
                f'Рост: {self.grow_status}%\n'
                f'Состояние: {self.get_health_status()}\n'
                f'Посажено в {default_hrs(self.life_time)}:{default_mns(self.life_time)}\n'
                f'Находится в Оранжерее: {default_hrs(self.life)}:{default_mns(self.life)}\n'
                f'{self.evol_status}'
                )
        if 1 <= self.health < 3 and self.bad != None: string += f'\nСколько времени болеет: {default_hrs(self.bad)}:{default_mns(self.bad)}'
        if self.good != None and not self.death : string += f'\nСколько времени имеет положительные показатели при болезни: {default_hrs(self.good)}:{default_mns(self.good)}\n'
        return string
        
class AppleTree(Plant):
    
    GROW_TIME, GROW_CHANGE = Time(40), 2
    WATER_WASTE, SUN_WASTE = 10, 8

    max_water, min_water = 90, 10
    max_sun, min_sun = 60, 10

    grow_evolution = 80
    evol_days = 10
    catch_apples = None
    evol_status = 'Не плодоносит'

    def __init__(self, name, water, sun, time):
        super().__init__(name = name, water = water, sun = sun, time = time)
        self.apples = 0

    def evolution(self, time):
        apples = 0
        logs = ''
        if self.grow_status >= self.grow_evolution:
            global catch
            catch = True
            if (self.catch_apples == None and not self.death): 
                self.evol_status = 'Плодоносит'
                self.catch_apples = -1
                logs += (f'\n{' ' * 50}[{default_hrs(time)}:{default_mns(time)}]')
                logs += (f'\n---->{'*^*' * 2} Яблоня {self.name} достигла прогресса роста в {self.grow_evolution}%! Теперь она будет давать плоды 10 дней подряд! {'*^*' * 2}<----\n')

            if not self.death and (self.life - self.catch_apples > 1440 or self.catch_apples == -1):
                apples = random.randint(10, 20)
                self.evol_days -= 1 # Сколько дней еще будет плодоносить
                if self.evol_days == 0:
                    self.health = 0
                    self.death = True
                        
                    logs += (f'\n{' ' * 50}[{default_hrs(time)}:{default_mns(time)}]\n')
                    logs += (f'Яблоня дала {apples} плодов! Сегодня яблоня умерла')
                else:    
                    self.catch_apples = self.life
                    logs += (f'\n{' ' * 50}[{default_hrs(time)}:{default_mns(time)}]\n')
                    logs += (f'Сегодня яблоня дала {apples} плодов! Дней до естественной смерти: {self.evol_days}\n')
                
            return apples, logs
        else:
            return apples, logs

class Orchid(Plant):
    
    GROW_TIME, GROW_CHANGE = Time(20), 5
    WATER_WASTE, SUN_WASTE = 5, 10

    max_water, min_water = 55, 15
    max_sun, min_sun = 80, 30

    grow_evolution = 90
    evol_days = 2
    catch_bud = None
    catch_days = None
    evol_status = 'Не имеет лепестков'

    def __init__(self, name, water, sun, time):
        super().__init__(name = name, water = water, sun = sun, time = time)
        self.bud_color = None
    
    def evolution(self, time:Time = 0):
        logs = ''
        if self.grow_status >= self.grow_evolution and not self.death:
            global catch
            catch = True
            if self.catch_bud == None:
                self.catch_bud = random.choice(['красными', 'желтыми', 'сиреневыми', 'белыми'])
                self.evol_status = f'Укарашает оранжерею {self.catch_bud} лепестками'

                logs += (f'\n{' ' * 50}[{default_hrs(time)}:{default_mns(time)}]')
                logs += (f'\n---->{'*^*' * 2} Орхидея {self.name} достигла прогресса роста в {self.grow_evolution}! Теперь она будет украшать оранжерею {self.catch_bud} лепестками! {'*^*' * 2}<----\n')
            if self.grow_status >= 100:
                if self.catch_days == None: 
                    self.catch_days = self.life
                    self.evol_days -= 1
                    logs += (f'\n{' ' * 50}[{default_hrs(time)}:{default_mns(time)}]')
                    logs += (f'\n{' ' * 20}{'&' * 4}   [Орхидея {self.name} умрет естественной смертью через {self.evol_days} дней]   {'&' * 4}\n')

                if self.life - self.catch_days >= 1440:
                    self.catch_days = self.life
                    self.evol_days -= 1
                    if self.evol_days == 0:
                        
                        self.health = 0
                        self.death = True
                        
                        logs += (f'\n[{default_hrs(time)}:{default_mns(time)}]Орхидея {self.name} умерла естественной смертью!')
                        return self.catch_bud, logs
                    else:
                        logs += (f'\n{' ' * 50}[{default_hrs(time)}:{default_mns(time)}]')
                        logs += (f'\n{' ' * 20}{'&' * 4}   [Орхидея {self.name} умрет естественной смертью через {self.evol_days} дней]   {'&' * 4}\n')
            return self.catch_bud, logs
        else: return self.catch_bud, logs

